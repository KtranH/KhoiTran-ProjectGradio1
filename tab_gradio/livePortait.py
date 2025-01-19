import gradio as gr
from process.genImage import generate_image

def check_inputs(input_image):
    return gr.Button(interactive=True) if input_image is not None else gr.Button(interactive=False)
def tab5_interface():
    with gr.Blocks() as tab5:
        with gr.Row():
            with gr.Column():
                rotate_pitch = gr.Slider(label="Ngẩng đầu lên xuống (Ngẩng xuống:  số âm, Ngẩng lên: số dương)", value=0, maximum=20, minimum=-20, step=1)
                rotate_yaw = gr.Slider(label="Quay mặt sang 2 bên (Quay trái: số âm, Quay phải: số dương)", value=0, maximum=20, minimum=-20, step=1)
                rotate_roll = gr.Slider(label="Lăn đầu sang 2 bên (Lăn trái: số âm, Lăn phải: số dương)", value=0, maximum=20, minimum=-20, step=1)
                blink = gr.Slider(label="Nháy mắt (Nhắm mắt: số âm, Mở mắt: số dương)", value=0, maximum=20, minimum=-20, step=1)
                eyebrow = gr.Slider(label="Nhấc lông mày (Nhấc xuống: số âm, Nhấc lên: số dương)", value=0, maximum=15, minimum=-10, step=1)
                wink = gr.Slider(label="Nháy mắt một bên (Nhắm mắt: số âm, Mở mắt: số dương)", value=0, maximum=20, minimum=0, step=1)
                pupil_x = gr.Slider(label="Di chuyển đồng tử theo chiều ngang (Trái: số âm, Phải: số dương)", value=0, maximum=15, minimum=-15, step=1)
                pupil_y = gr.Slider(label="Di chuyển đồng tử theo chiều dọc (Xuống: số âm, Lên: số dương)", value=0, maximum=15, minimum=-15, step=1)
                aaa = gr.Slider(label="Mở miệng dạng aaa (Kép miệng: số âm, Mở miệng: số dương)", value=0, maximum=15, minimum=-15, step=1)
                eee = gr.Slider(label="Co dãn miệng dạng eee (Co miệng: số âm, Dãn miệng: số dương)", value=0, maximum=15, minimum=-15, step=1)
                woo = gr.Slider(label="Co dãn miệng dạng woo (Co miệng: số âm, Dãn miệng: số dương)", value=0, maximum=15, minimum=-15, step=1)
                smile = gr.Slider(label="Mỉm cười (Không cười: số âm, Mỉm cười: số dương)", value=0, maximum=1.3, minimum=-0.3, step=0.3)         
            with gr.Column():
                input_image = gr.Image(label="Tải ảnh lên", type="numpy", height=834, width=768)
        submit_btn = gr.Button("Tạo ảnh 📷", interactive=False)
        with gr.Row():
            output_image = gr.Image(label="Ảnh đầu ra", height=768, width=768, interactive=False)

    #Kiểm tra tải ảnh
    input_image.input(
        fn=check_inputs, 
        inputs=[input_image], 
        outputs=[submit_btn]
    )
    #Xử lý nút tạo ảnh
    submit_btn.click(
        fn=generate_image, 
        inputs=[input_image, rotate_pitch, rotate_yaw, rotate_roll, blink, eyebrow, wink, pupil_x, pupil_y, aaa, eee, woo, smile], 
        outputs=output_image
    )
    return tab5
