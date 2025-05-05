import gradio as gr
import requests
import json
import io
from PIL import Image
import base64
import re
from src.utils.database import DatabaseConnection
from src.utils.query_generator import QueryGenerator
import os
from typing import Dict, Any, Optional
from src.config.database import get_connection_string

# Khởi tạo kết nối database
DB_CONNECTION_STRING = get_connection_string()
db = DatabaseConnection(DB_CONNECTION_STRING)

# Cache cho schema của các bảng
table_schemas = {}

def init_table_schemas():
    """Khởi tạo schema cho các bảng"""
    global table_schemas
    if db.connect():
        try:
            # Lấy danh sách các bảng
            results = db.execute_query("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            
            if results:
                for table in results:
                    table_name = table["TABLE_NAME"]
                    schema = db.get_table_schema(table_name)
                    if schema:
                        table_schemas[table_name] = schema
                print(f"Đã tải schema cho {len(table_schemas)} bảng")
            else:
                print("Không tìm thấy bảng nào trong database")
        except Exception as e:
            print(f"Lỗi khi khởi tạo schema: {str(e)}")
        finally:
            db.disconnect()
    else:
        print("Không thể kết nối đến database")

# Khởi tạo schema khi khởi động
init_table_schemas()

# Khởi tạo QueryGenerator
query_generator = QueryGenerator(table_schemas)

def extract_think_content(response):
    think_pattern = r'<think>(.*?)</think>'
    main_pattern = r'</think>\s*(.*?)$'
    
    think_match = re.search(think_pattern, response, re.DOTALL)
    main_match = re.search(main_pattern, response, re.DOTALL)
    
    think_content = think_match.group(1).strip() if think_match else None
    main_content = main_match.group(1).strip() if main_match else response.strip()
    
    return think_content, main_content

def search_web(query: str) -> str:
    """
    Tìm kiếm thông tin trên web (sử dụng DuckDuckGo API)
    """
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json"
            }
        )
        data = response.json()
        if data.get("Abstract"):
            return data["Abstract"]
        elif data.get("RelatedTopics"):
            return data["RelatedTopics"][0].get("Text", "Không tìm thấy thông tin phù hợp.")
        return "Không tìm thấy thông tin phù hợp."
    except Exception as e:
        return f"Lỗi khi tìm kiếm: {str(e)}"

def is_database_question(question: str) -> bool:
    """
    Kiểm tra xem câu hỏi có liên quan đến database không
    """
    # Các từ khóa liên quan đến database
    db_keywords = [
        "database", "cơ sở dữ liệu", "sql", "bảng", "table",
        "có bao nhiêu", "số lượng", "danh sách", "list",
        "phòng", "room", "loại phòng", "room type",
        "trống", "available", "đã đặt", "booked",
        "khách hàng", "customer", "đơn đặt", "booking",
        "tìm kiếm trong database", "tra cứu", "query"
    ]
    
    question = question.lower()
    return any(keyword.lower() in question for keyword in db_keywords)

def process_database_query(question: str) -> Optional[str]:
    """
    Xử lý câu hỏi liên quan đến database
    """
    if not is_database_question(question):
        return None
        
    # Phân tích câu hỏi
    analysis = query_generator.analyze_question(question)
    if not analysis:
        return "Tôi hiểu bạn đang hỏi về database, nhưng tôi không thể xác định được bảng hoặc thông tin cần truy vấn. Vui lòng thử lại với câu hỏi cụ thể hơn."
        
    # Tạo câu truy vấn SQL
    query = query_generator.generate_sql_query(analysis)
    print(f"SQL Query: {query}")  # In ra câu truy vấn để debug
    
    # Thực thi truy vấn
    if db.connect():
        try:
            results = db.execute_query(query)
            if results is not None:
                return f"""🔍 **Kết quả truy vấn database:**
```sql
{query}
```

📊 **Dữ liệu:**
{db.format_results_as_text(results)}"""
            return "Không tìm thấy dữ liệu phù hợp."
        except Exception as e:
            return f"Lỗi khi truy vấn database: {str(e)}"
        finally:
            db.disconnect()
    return "Không thể kết nối đến database."

def get_chat_response(message, history, enable_web_search=False, api_url="http://127.0.0.1:1234"):
    headers = {
        "Content-Type": "application/json",
    }
    
    # Kiểm tra xem có phải câu hỏi về database không
    db_result = process_database_query(message)
    if db_result:
        return {
            "think": f"Đã tìm thấy thông tin trong database. Đang xử lý kết quả...",
            "main": db_result
        }
    
    # Chuyển đổi lịch sử chat sang định dạng phù hợp cho API
    conversation_history = []
    for msg in history:
        conversation_history.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    conversation_history.append({"role": "user", "content": message})
    
    payload = {
        "messages": conversation_history,
        "temperature": 0.8,
        "max_tokens": 4096,
    }
    
    try:
        response = requests.post(f"{api_url}/v1/chat/completions", 
                               headers=headers, 
                               json=payload,
                               timeout=300)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Xử lý nội dung think và main
        think_content, main_content = extract_think_content(content)
        
        # Chỉ tìm kiếm web khi được bật và có yêu cầu tìm kiếm
        if enable_web_search and ("tìm trên web" in message.lower() or "tìm kiếm" in message.lower()):
            web_result = search_web(message)
            if think_content:
                think_content += f"\n\n🌐 **Kết quả tìm kiếm web:**\n{web_result}"
            else:
                think_content = f"🌐 **Kết quả tìm kiếm web:**\n{web_result}"
        
        if think_content:
            return {
                "think": think_content,
                "main": main_content
            }
        return main_content
    except Exception as e:
        return f"Lỗi: {str(e)}"

def analyze_image(image, question, history, api_url="http://127.0.0.1:1234"):
    if image is None:
        return "Vui lòng tải lên một hình ảnh để phân tích.", history
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    headers = {
        "Content-Type": "application/json",
    }
    
    conversation_history = []
    for msg in history:
        content = msg["content"]
        if isinstance(content, dict) and "main" in content:
            content = content["main"]
        conversation_history.append({"role": msg["role"], "content": content})
    
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": question},
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{img_str}"
            }
        ]
    }
    
    payload = {
        "messages": conversation_history + [message],
        "temperature": 0.7,
        "max_tokens": 1024,
    }
    
    try:
        response = requests.post(f"{api_url}/v1/chat/completions", 
                               headers=headers, 
                               json=payload,
                               timeout=30)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Xử lý nội dung think và main
        think_content, main_content = extract_think_content(content)
        assistant_message = {
            "role": "assistant",
            "content": {
                "think": think_content,
                "main": main_content
            } if think_content else main_content
        }
        return assistant_message["content"], history + [
            {"role": "user", "content": question},
            assistant_message
        ]
    except Exception as e:
        return f"Lỗi khi phân tích ảnh: {str(e)}", history

def create_chat_message(role, content):
    return {"role": role, "content": content}

def process_image_and_question(image, question, history, enable_web_search=False):
    """
    Xử lý câu hỏi liên quan đến hình ảnh
    """
    if not question.strip():
        return history if history else []
    if history is None:
        history = []
    
    # Thêm tin nhắn của user theo đúng định dạng
    history.append({"role": "user", "content": question})
    
    if image is None:
        history.append({"role": "assistant", "content": "Vui lòng tải lên một hình ảnh để phân tích."})
        return history
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Tạo tin nhắn với hình ảnh
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": question},
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{img_str}"
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "messages": [message],
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=30
        )
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Xử lý nội dung think và main
        think_content, main_content = extract_think_content(content)
        
        # Thêm kết quả tìm kiếm web nếu được yêu cầu
        if enable_web_search and ("tìm trên web" in question.lower() or "tìm kiếm" in question.lower()):
            web_result = search_web(question)
            if think_content:
                think_content += f"\n\n🌐 **Kết quả tìm kiếm web:**\n{web_result}"
            else:
                think_content = f"🌐 **Kết quả tìm kiếm web:**\n{web_result}"
        
        # Tạo nội dung phản hồi
        if think_content:
            bot_content = f"""🤔 **Suy nghĩ:**
{think_content}

😃 **Trả lời:**
{main_content}"""
        else:
            bot_content = main_content
        
        # Thêm tin nhắn của bot theo đúng định dạng
        history.append({"role": "assistant", "content": bot_content})
        return history
    except Exception as e:
        history.append({"role": "assistant", "content": f"Lỗi khi phân tích ảnh: {str(e)}"})
        return history

def tab6_interface():
    with gr.Blocks() as tab6:
        gr.Markdown("### 🤖 Chatbot AI")
        
        with gr.Row():
            with gr.Column(scale=8):
                chatbot = gr.Chatbot(
                    type="messages",
                    height=600,
                    show_label=False,
                    container=True,
                    avatar_images=("https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/476116956_637530651994945_4137383568616611950_n.jpg", "https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/images.jpg"),
                    latex_delimiters=[
                        {"left": "\\[", "right": "\\]", "display": True},
                        {"left": "\\(", "right": "\\)", "display": False},
                        {"left": "$", "right": "$", "display": False},
                        {"left": "\\boxed{", "right": "}", "display": False}
                    ],
                    bubble_full_width=False,
                    show_copy_button=True,
                    render_markdown=True
                )
            with gr.Column(scale=3, visible=False): 
                image_input = gr.Image(label="Tải lên hình ảnh để phân tích", type="pil")
        
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    label="Nhập tin nhắn của bạn",
                    placeholder="Nhập tin nhắn (ấn enter để gửi tin nhắn)...",
                    show_label=False
                )
            with gr.Column(scale=1):
                clear = gr.Button("🗑️ Xóa")
        
        with gr.Row():
            enable_web_search = gr.Checkbox(
                label="Bật tìm kiếm web",
                value=False,
                info="Khi bật, chatbot sẽ tìm kiếm thông tin trên web nếu được yêu cầu"
            )
        
        def user(user_message, history):
            if history is None:
                history = []
            # Tạo tin nhắn theo đúng định dạng của Gradio
            history.append({"role": "user", "content": user_message})
            return "", history

        def bot(history, enable_web_search):
            if not history:
                return history
            
            # Lấy tin nhắn cuối cùng của user
            user_message = history[-1]["content"]
            
            # Chuyển đổi lịch sử chat sang định dạng phù hợp cho API
            formatted_history = []
            for msg in history[:-1]:  # Không bao gồm tin nhắn cuối cùng vì đã lấy ở trên
                formatted_history.append(msg)
            
            # Lấy phản hồi từ bot
            bot_message = get_chat_response(user_message, formatted_history, enable_web_search)
            
            # Tạo tin nhắn bot theo đúng định dạng
            if isinstance(bot_message, dict) and "think" in bot_message:
                content = f"""🤔 **Suy nghĩ:**
{bot_message['think']}

---

😃 **Trả lời:**
{bot_message['main']}"""
            else:
                content = bot_message
            
            # Thêm tin nhắn của bot vào lịch sử
            history.append({"role": "assistant", "content": content})
            return history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, [chatbot, enable_web_search], chatbot
        )

        clear.click(lambda: [], None, chatbot, queue=False)
        
        # Xử lý khi người dùng gửi tin nhắn với hình ảnh
        msg.submit(
            process_image_and_question,
            [image_input, msg, chatbot, enable_web_search],
            [chatbot],
        )

    return tab6