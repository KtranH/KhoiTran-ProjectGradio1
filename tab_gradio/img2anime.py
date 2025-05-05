import gradio as gr
import time
from process.genImage import generate_image_ImgToImg
from process.create_seed import update_seed

def check_inputs(input_image, seed_number):
    return gr.Button(interactive=True) if input_image is not None and seed_number != "" else gr.Button(interactive=False)
def tab2_interface():
    with gr.Blocks() as tab2:
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Tải ảnh lên", type="numpy", height=512, width=768)
            with gr.Column():
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                seed_number = gr.Number(label="Seed", value=99123456999)
                random_seed_btn = gr.Button("Tạo seed 📱")
                gr.Markdown("Nếu bạn không biết cách sử dụng hãy đọc hướng dẫn sử dụng.")
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)

    # Xử lý nút tạo seed
    random_seed_btn.click(
        fn=update_seed, 
        inputs=[], 
        outputs=[seed_number]
    )

    # Kiểm tra đầu vào
    input_image.input(
        fn=check_inputs, 
        inputs=[input_image, seed_number], 
        outputs=[submit_btn]
    )

    # Hàm tạo ảnh với progress bar
    def generate_image_with_progress(seed_number, input_image, width_slider, height_slider, progress=gr.Progress()): 
        for i in range(80):
            progress(i/100, desc="Đang tạo ảnh...")
            time.sleep(5/80)                 
        image = generate_image_ImgToImg(seed_number, input_image, width_slider, height_slider)
        time.sleep(1)
        progress(1.0, desc="Hoàn thành!")
            
        return image
    
    # Xử lý nút tạo ảnh
    submit_btn.click(
        fn=generate_image_with_progress, 
        inputs=[seed_number, input_image, width_slider, height_slider], 
        outputs=output_image
    )
    return tab2
