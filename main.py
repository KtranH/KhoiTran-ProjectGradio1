import gradio as gr
from tab_gradio.text2image import tab1_interface
from tab_gradio.img2anime import tab2_interface
from tab_gradio.instantID import tab3_interface

with gr.Blocks(theme='argilla/argilla-theme', title='Khôi Trần - AI') as demo:
    with gr.Row():
        gr.Markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="https://scontent.fsgn5-15.fna.fbcdn.net/v/t39.30808-1/414203916_385731537174859_3046328303491009574_n.jpg?stp=c0.180.943.943a_dst-jpg_s160x160_tt6&_nc_cat=111&ccb=1-7&_nc_sid=e99d92&_nc_ohc=VsaQ1HabhDgQ7kNvgGF0bOq&_nc_zt=24&_nc_ht=scontent.fsgn5-15.fna&_nc_gid=A5JNss35NBFWueAywFpaRtA&oh=00_AYC4Ggti_5XBzCJUKmPuMs0cjZMZVGiezZ_UngXfebPWRg&oe=678DAF6F" width="60px" style="border-radius: 50%;">
                <h1>Tạo ảnh với AI</h1>
            </div>
            """)
    gr.Markdown("### Được phát triển bởi Khôi Trần")

    with gr.Tab("Tạo ảnh bằng văn bản"):
        tab1_interface()
    with gr.Tab("Tạo ảnh sang anime"):
        tab2_interface()
    with gr.Tab("Tạo ảnh sao chép khuôn mặt"):
        tab3_interface()

    gr.Markdown("#### Lưu ý ⚠️")
    gr.Markdown("* Seed là một số ngẫu nhiên giúp mô hình tạo ra ảnh theo cách khác nhau. Bạn có thể nhập số bất kỳ hoặc nhấn vào nút để tạo số ngẫu nhiên.")
    gr.Markdown("* Chiều rộng và chiều cao ảnh sẽ ảnh hưởng đến chất lượng ảnh. Bạn có thể thử nghiệm với các giá trị khác nhau.")
    gr.Markdown("* Bạn có thể mô tả bằng tiếng anh hoặc tiếng việt. Ví dụ như: **A cat in the forest** hoặc **Một con mèo trong rừng**.")
    gr.Markdown("* Đang trong quá trình phát triển nên vẫn có lỗi! Vui lòng không nhập vào từ khóa nhạy cảm.")

    gr.Markdown("#### Thông tin 📝")
    gr.Markdown("")
if __name__ == "__main__":
    demo.launch(show_api=False)
