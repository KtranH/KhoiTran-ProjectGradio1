import gradio as gr
import requests
import json
import io
from PIL import Image
import base64
import re

def extract_think_content(response):
    think_pattern = r'<think>(.*?)</think>'
    main_pattern = r'</think>\s*(.*?)$'
    
    think_match = re.search(think_pattern, response, re.DOTALL)
    main_match = re.search(main_pattern, response, re.DOTALL)
    
    think_content = think_match.group(1).strip() if think_match else None
    main_content = main_match.group(1).strip() if main_match else response.strip()
    
    return think_content, main_content

def get_chat_response(message, history, api_url="http://127.0.0.1:1234"):
    headers = {
        "Content-Type": "application/json",
    }
    
    conversation_history = []
    for msg in history:
        # Chỉ lấy nội dung chính, không lấy phần suy nghĩ
        content = msg["content"]
        if isinstance(content, dict) and "main" in content:
            content = content["main"]
        conversation_history.append({"role": msg["role"], "content": content})
    
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

def tab6_interface():
    with gr.Blocks() as tab6:
        gr.Markdown("### 🤖 Chatbot AI")
        
        with gr.Row():
            with gr.Column(scale=8):
                chatbot = gr.Chatbot(
                    height=800,
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
        
        def user(user_message, history):
            if history is None:
                history = []
            history.append([user_message, None])
            return "", history

        def bot(history):
            if not history:
                return history
            
            # Lấy tin nhắn cuối cùng của user
            user_message = history[-1][0]
            
            # Chuyển đổi lịch sử chat sang định dạng phù hợp
            formatted_history = []
            for h in history[:-1]:
                if h[1] is not None:  # Chỉ thêm các cuộc hội thoại đã hoàn thành
                    formatted_history.append(create_chat_message("user", h[0]))
                    formatted_history.append(create_chat_message("assistant", h[1]))
            
            # Lấy phản hồi từ bot
            bot_message = get_chat_response(user_message, formatted_history)
            
            # Xử lý phản hồi có think content
            if isinstance(bot_message, dict) and "think" in bot_message:
                think_part = f"🤔 **Suy nghĩ:**\n{bot_message['think']}\n\n---\n"
                main_part = f"😃 **Trả lời:**\n{bot_message['main']}"
                history[-1][1] = think_part + main_part
            else:
                history[-1][1] = bot_message
                
            return history

        def process_image_and_question(image, question, history):
            if not question.strip():
                return history if history else []
            if history is None:
                history = []
                
            # Thêm câu hỏi của user vào lịch sử
            history.append([question, None])
            
            # Chuyển đổi lịch sử chat sang định dạng phù hợp
            formatted_history = []
            for h in history[:-1]:
                if h[1] is not None:
                    formatted_history.append(create_chat_message("user", h[0]))
                    formatted_history.append(create_chat_message("assistant", h[1]))
            
            # Phân tích ảnh và nhận phản hồi
            response, _ = analyze_image(image, question, formatted_history)
            
            # Xử lý phản hồi có think content
            if isinstance(response, dict) and "think" in response:
                history[-1][1] = f"""🤔 **Suy nghĩ:**
                {response['think']}

                😃 **Trả lời:**
                {response['main']}"""
            else:
                history[-1][1] = response
                
            return history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )

        clear.click(lambda: [], None, chatbot, queue=False)
        
        msg.submit(
            process_image_and_question,
            [image_input, msg, chatbot],
            [chatbot],
        )

    return tab6