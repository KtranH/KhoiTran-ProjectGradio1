import gradio as gr

def tab3_interface():
    with gr.Blocks() as tab3:
        with gr.Row():
            with gr.Column():
                model_img = gr.Dropdown(label="Gợi ý phong cách tạo ảnh", choices=["Chân thật", "Sticker cute", "3D Chibi"], interactive=True)
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="Ngoài biển, cát...", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                seed_number = gr.Number(label="Seed", value=99123456999)
                random_seed_btn = gr.Button("Tạo seed 📱")
            with gr.Column():
                input_image = gr.Image(label="Tải ảnh lên", type="numpy", height=512, width=768)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)
    return tab3
