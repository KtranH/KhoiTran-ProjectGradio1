import gradio as gr

#Thông báo thực thi chức năng
def notification_info():
    gr.Info("Đang thực thi chức năng...", duration=3)
#Thông báo cảnh báo
def notification_warning():
    gr.Warning("Vui lòng không nhập từ khóa nhạy cảm!", duration=3)
#Thông báo lỗi
def notification_error():
    gr.Error("Đã xảy ra lỗi! Vui lòng thử lại.", duration=3)