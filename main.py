import gradio as gr
from tab_gradio.text2image import tab1_interface
from tab_gradio.img2anime import tab2_interface
from tab_gradio.instantID import tab3_interface
from tab_gradio.livePortait import tab5_interface
from tab_gradio.chatbot import tab6_interface
from tab_gradio.how_to_use import tab7_interface
#from tab_gradio.coupleAvatar import tab4_interface
from process.notification import notification_info, notification_warning, notification_warning_load, notification_error

def on_load():
    notification_warning_load()

with gr.Blocks(theme='ParityError/Interstellar', title='Khôi Trần - AI') as demo:
    demo.load(on_load)
    # Header
    with gr.Row():
            gr.Markdown(
                """
                <div style="position: fixed; top: 0; z-index: 1000; background-color: black; padding: 10px; display: flex; align-items: center; gap: 10px; padding: 5px; margin-bottom: 100px; width: 90%;">
                    <img src="https://scontent.fsgn5-15.fna.fbcdn.net/v/t39.30808-1/414203916_385731537174859_3046328303491009574_n.jpg?stp=c0.180.943.943a_dst-jpg_s200x200_tt6&_nc_cat=111&ccb=1-7&_nc_sid=e99d92&_nc_ohc=6xTMlIxSmG4Q7kNvgG2-F4r&_nc_zt=24&_nc_ht=scontent.fsgn5-15.fna&_nc_gid=A-ZJ18nsRPPzpLKLPJthVW1&oh=00_AYDtJtE2qNrwRVz0fADze1EZH687dC_Ah6bugfHMY1X_Jw&oe=67939E2F" 
                    width="60px" style="border-radius: 50%;">
                    <div>
                        <div class="header">
                            <h1>Sáng tạo ảnh với AI 🎨</h1>
                            <p>Phát triển bởi Khôi Trần</p>
                        </div>
                    </div>
                </div>
                """
            )
            gr.Markdown(
                """
                <div style="padding-top: 80px;">
                """
            )
    gr.Markdown("### Chào mừng bạn đến với ứng dụng tạo ảnh với AI. Hãy chọn một trong những chức năng dưới đây để bắt đầu.")
    gr.Markdown(
        """
            <div style="padding-top: 5px;">
        """
        )

    # Tabs
    with gr.Tab("Tạo ảnh bằng văn bản"):
        tab1_interface()
    with gr.Tab("Tạo ảnh sticker từ khuôn mặt của bạn"):
        tab2_interface()
    with gr.Tab("Tạo ảnh sao chép khuôn mặt"):
        tab3_interface()
    with gr.Tab("Thay đổi biểu cảm khuôn mặt"):
        tab5_interface()
    #with gr.Tab("Tạo avatar cặp đôi"):
    #    tab4_interface()
    with gr.Tab("Chatbot"):
        tab6_interface()
    with gr.Tab("Hướng dẫn sử dụng"):
        tab7_interface()

    # Footer
    gr.Markdown("### Lưu ý ⚠️")
    gr.Markdown("* Seed là một số ngẫu nhiên giúp mô hình tạo ra ảnh theo cách khác nhau. Bạn có thể nhập số bất kỳ hoặc nhấn vào nút để tạo số ngẫu nhiên.")
    gr.Markdown("* Chiều rộng và chiều cao ảnh sẽ ảnh hưởng đến chất lượng ảnh. Bạn có thể thử nghiệm với các giá trị khác nhau.")
    gr.Markdown("* Bạn có thể mô tả bằng tiếng anh hoặc tiếng việt. Ví dụ như: **A cat in the forest** hoặc **Một con mèo trong rừng**.")
    gr.Markdown("* Đang trong quá trình phát triển nên vẫn có lỗi! Vui lòng không nhập vào từ khóa nhạy cảm.")

    gr.Markdown("### Thông tin 📝")
    gr.Markdown("* Người phát triển 👨‍💻: [Khôi Trần](https://www.facebook.com/profile.php?id=100072140473156)")
    gr.Markdown("* Mã nguồn 📦: [GitHub](https://github.com/KtranH/KhoiTran-ProjectGradio1.git)")
    gr.Markdown("* Liên hệ 📧: hoangkhoi230@gmail.com")
if __name__ == "__main__":
    demo.launch(show_api=False)
