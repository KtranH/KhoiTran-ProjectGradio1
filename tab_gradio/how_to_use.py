import gradio as gr

def tab8_interface():
    with gr.Blocks() as tab8:
        gr.Markdown("# Tạo ảnh bằng văn bản (Text-to-Image) 📜")
        gr.Markdown(" - Bạn có thể tạo ảnh từ mô tả của mình. Mô tả của bạn sẽ được chuyển đổi thành ảnh.")
        gr.Markdown(" - Gợi ý mô tả: 'Một cô gái đang ngồi trên bãi biển, nắng vàng rực rỡ, sóng biển nhẹ nhàng.'")
        gr.Markdown(" - Để có kết quả tốt nhất, bạn nên chọn mô tả chi tiết và rõ ràng, kích thướt ảnh tốt nhất là 512x768.")
        gr.Markdown("![text-to-image](https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/857f6a3f-2cb2-4dd3-8f27-c265dbc66cee.jpg)")
        gr.Markdown("# Tạo ảnh sang anime (Anime Style Transfer) 🎨")
        gr.Markdown(" - Bạn có thể chuyển đổi ảnh của mình sang phong cách anime.")
        gr.Markdown(" - Gợi ý ảnh: Ảnh chân dung, ảnh cảnh biển, ảnh cảnh đô thị, ảnh cảnh thiên nhiên.")
        gr.Markdown(" - Để có kết quả tốt nhất, bạn nên chọn ảnh chất lượng cao, kích thướt ảnh tốt nhất là 512x768.")
        gr.Markdown("![anime-style-transfer](https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/857f6a3f-2cb2-4dd3-8f27-c265dbc66cee.jpg)")
        gr.Markdown("# Sao chép khuôn mặt (Face Swapping) 🎉")
        gr.Markdown(" - Bạn có thể sao chép khuôn mặt của mình vào ảnh khác.")
        gr.Markdown(" - Gợi ý ảnh: Ảnh chân dung, cận mặt, càng rõ mặt càng tốt.")
        gr.Markdown(" - Để có kết quả tốt nhất, bạn nên chọn ảnh chất lượng cao, kích thướt ảnh tốt nhất là 512x768 và độ chân thực nên là 0.8.")
        gr.Markdown("![face-swapping](https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/857f6a3f-2cb2-4dd3-8f27-c265dbc66cee.jpg)")
        gr.Markdown("# Thay đổi biểu cảm khuôn mặt (Emotion Transfer) 😂")
        gr.Markdown(" - Bạn có thể thay đổi biểu cảm khuôn mặt của mình.")
        gr.Markdown(" - Gợi ý ảnh: Ảnh chân dung, cận mặt, càng rõ mặt càng tốt.")
        gr.Markdown(" - Để có kết quả tốt nhất, bạn nên chọn ảnh chất lượng cao.")
        gr.Markdown("![emotion-transfer](https://pub-ed515111f589440fb333ebcd308ee890.r2.dev/857f6a3f-2cb2-4dd3-8f27-c265dbc66cee.jpg)")
    return tab8
