import gradio as gr

def tab5_interface():
    with gr.Blocks() as tab5:
        with gr.Row():
            with gr.Column():
                rotate_pitch = gr.Slider(label="Ngẩng đầu lên xuống (Ngẩng xuống:  số âm, Ngẩng lên: số dương)", value=0, maximum=20, minimum=-20, step=1)
                rotate_yaw = gr.Slider(label="Quay mặt sang 2 bên (Quay trái: số âm, Quay phải: số dương)", value=0, maximum=20, minimum=-20, step=1)
                rotate_roll = gr.Slider(label="Lăn đầu sang 2 bên (Lăn trái: số âm, Lăn phải: số dương)", value=0, maximum=20, minimum=-20, step=1)
                blink = gr.Slider(label="Nháy mắt (Nhắm mắt: số âm, Mở mắt: số dương)", value=0, maximum=20, minimum=-20, step=1)
                eyebrow = gr.Slider(label="Nhấc lông mày (Nhấc xuống: số âm, Nhấc lên: số dương)", value=0, maximum=20, minimum=-20, step=1)
                wink = gr.Slider(label="Nháy mắt một bên (Nhắm mắt: số âm, Mở mắt: số dương)", value=0, maximum=20, minimum=0, step=1)
                pupil_x = gr.Slider(label="Di chuyển đồng tử theo chiều ngang (Trái: số âm, Phải: số dương)", value=0, maximum=20, minimum=-20, step=1)
                pupil_y = gr.Slider(label="Di chuyển đồng tử theo chiều dọc (Xuống: số âm, Lên: số dương)", value=0, maximum=20, minimum=-20, step=1)
                aaa = gr.Slider(label="Mở miệng dạng aaa (Kép miệng: số âm, Mở miệng: số dương)", value=0, maximum=20, minimum=-20, step=1)
                eee = gr.Slider(label="Co dãn miệng dạng eee (Co miệng: số âm, Dãn miệng: số dương)", value=0, maximum=20, minimum=-20, step=1)
                woo = gr.Slider(label="Co dãn miệng dạng woo (Co miệng: số âm, Dãn miệng: số dương)", value=0, maximum=15, minimum=-15, step=1)
                smile = gr.Slider(label="Mỉm cười (Không cười: số âm, Mỉm cười: số dương)", value=0, maximum=20, minimum=-20, step=1)         
            with gr.Column():
                input_image = gr.Image(label="Tải ảnh lên", type="numpy", height=1000, width=768)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            output_image = gr.Image(label="Ảnh đầu ra", height=512, width=768, interactive=False)
    return tab5
