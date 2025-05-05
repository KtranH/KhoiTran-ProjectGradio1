import gradio as gr
import time
from process.create_seed import update_seed
from process.genImage import generate_image_TextToImage

css = """
    button#seed_btn {
        background-color: red !important;
    }
}
"""

def check_inputs(prompt_text, seed_number):
    return gr.Button(interactive=True) if prompt_text != "" and seed_number != "" else gr.Button(interactive=False)
def tab1_interface():
    with gr.Blocks(css=css) as tab1:
        with gr.Row():
            with gr.Column():
                model_img = gr.Dropdown(label="Gợi ý phong cách tạo ảnh", choices=["Chân thực", "Hoạt hình", "3D cute"], interactive=True)
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="a girl, cute girl, simple background, white background... (Chưa có bộ lọc ảnh NSFW. Vui lòng không nhập từ nhậy cảm))", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                seed_number = gr.Number(label="Thông số Seed", value=99123456999, interactive=True)
                random_seed_btn = gr.Button("Tạo seed 📱", elem_id="seed_btn")
                gr.Markdown("Nếu bạn không biết cách sử dụng hãy đọc hướng dẫn sử dụng.")
            with gr.Row():
                output_image = gr.Image(label="Ảnh đầu ra", height=500, width=768, interactive=False)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
    
    # Xử lý nút tạo seed
    random_seed_btn.click(
        fn=update_seed, 
        inputs=[], 
        outputs=[seed_number]
    )

    # Kiểm tra đầu vào
    prompt_text.change(
        fn=check_inputs, 
        inputs=[prompt_text, seed_number], 
        outputs=[submit_btn]
    )
    
    # Hàm tạo ảnh với progress bar
    def generate_image_with_progress(seed, prompt, width, height, model, progress=gr.Progress()):     
        for i in range(80):
            progress(i/100, desc="Đang tạo ảnh...")
            time.sleep(5/80)             
        image = generate_image_TextToImage(seed, prompt, width, height, model)
        time.sleep(1)
        progress(1.0, desc="Hoàn thành!")
            
        return image

    # Xử lý nút tạo ảnh
    submit_btn.click(
        fn=generate_image_with_progress, 
        inputs=[seed_number, prompt_text, width_slider, height_slider, model_img], 
        outputs=output_image
    )
    return tab1
