import gradio as gr

def tab1_interface():
    with gr.Blocks() as tab1:
        with gr.Row():
            with gr.Column():
                model_img = gr.Dropdown(label="Gợi ý phong cách tạo ảnh", choices=["Chân thật", "Hoạt hình", "3D cute"], interactive=True)
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="Ngoài biển, cát...", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                seed_number = gr.Number(label="Thông số Seed", value=99123456999, interactive=True)
                random_seed_btn = gr.Button("Tạo seed 📱")
            with gr.Row():
                output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
    return tab1
