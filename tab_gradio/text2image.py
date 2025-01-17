import gradio as gr

css = """
    button#seed_btn {
        background-color: red !important;
    }
}
"""

def tab1_interface():
    with gr.Blocks(css=css) as tab1:
        with gr.Row():
            with gr.Column():
                model_img = gr.Dropdown(label="Gợi ý phong cách tạo ảnh", choices=["Chân thật", "Hoạt hình", "3D cute"], interactive=True)
                prompt_text = gr.Textbox(label="Mô tả của bạn", placeholder="Ngoài biển, cát... (Chưa có bộ lọc ảnh NSFW. Vui lòng không nhập từ nhậy cảm)", lines=5)
                width_slider = gr.Slider(label="Chiều rộng", value=512, maximum=1024, minimum=256, step=64)
                height_slider = gr.Slider(label="Chiều cao", value=768, maximum=1024, minimum=256, step=64)
                seed_number = gr.Number(label="Thông số Seed", value=99123456999, interactive=True)
                random_seed_btn = gr.Button("Tạo seed 📱", elem_id="seed_btn")
            with gr.Row():
                output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
    return tab1
