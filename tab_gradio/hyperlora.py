import gradio as gr
import time
from process.genImage import generate_instant_id_hyperlora
from process.create_seed import update_seed

def check_inputs(input_image, prompt_text, seed_number):
    return gr.Button(interactive=True) if input_image is not None and prompt_text != "" and seed_number != "" else gr.Button(interactive=False)
def tab7_interface():
    with gr.Blocks() as tab7:
        with gr.Row():
            with gr.Column():
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="Ngoài biển, cát... (Chưa có bộ lọc ảnh NSFW. Vui lòng không nhập từ nhậy cảm)", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                hyper_lora_slider = gr.Slider(label="Độ chân thực", value=0.8, maximum=1, minimum=0, step=0.1)
                seed_number = gr.Number(label="Seed", value=99123456999)
                random_seed_btn = gr.Button("Tạo seed 📱")
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Tải ảnh lên khuôn mặt", type="numpy", height=500, width=768)
                input_image2 = gr.Image(label="Tải ảnh lên vóc dáng", type="numpy", height=500, width=768)
            output_image = gr.Image(label="Ảnh đầu ra", height=1012, width=768, interactive=False)

        # Xử lý nút tạo seed
        random_seed_btn.click(
            fn=update_seed, 
            inputs=[], 
            outputs=[seed_number]
        )

        # Kiểm tra đầu vào
        input_image.input(
            fn=check_inputs, 
            inputs=[input_image, prompt_text, seed_number], 
            outputs=[submit_btn]
        )
        input_image2.input(
            fn=check_inputs, 
            inputs=[input_image2, prompt_text, seed_number], 
            outputs=[submit_btn]
        )

        # Hàm tạo ảnh với progress bar
        def generate_image_with_progress(seed_number, input_image, input_image2, prompt_text, width_slider, height_slider, hyper_lora_slider, progress=gr.Progress()):                  
            for i in range(80):
                progress(i/100, desc="Đang tạo ảnh...")
                time.sleep(5/80)
            image = generate_instant_id_hyperlora(seed_number, input_image, input_image2, prompt_text, width_slider, height_slider, hyper_lora_slider)
            time.sleep(1)
            progress(1.0, desc="Hoàn thành!")
                
            return image

        # Xử lý nút tạo ảnh
        submit_btn.click(
            fn=generate_image_with_progress, 
            inputs=[seed_number, input_image, input_image2, prompt_text, width_slider, height_slider, hyper_lora_slider], 
            outputs=[output_image]
        )
    return tab7
