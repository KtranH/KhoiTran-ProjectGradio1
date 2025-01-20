import gradio as gr

def tab4_interface():
    with gr.Blocks() as tab4:
        with gr.Row():
            with gr.Column():
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="This two-panel image presents a boy and a girl, [LEFT] a boy, while [RIGHT] a girl, creating a fun Pixar scene, clear background, white background. ", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)
    return tab4
