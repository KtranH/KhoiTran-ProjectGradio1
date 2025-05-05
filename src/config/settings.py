"""
Cấu hình chung cho ứng dụng Gradio
"""

# Cấu hình giao diện
UI_CONFIG = {
    'theme': 'ParityError/Interstellar',
    'title': 'Khôi Trần - AI'
}

# Cấu hình đường dẫn
PATHS = {
    'input_dir': 'input',
    'output_dir': 'output',
    'assets_dir': 'assets'
}

# Cấu hình model
MODEL_CONFIG = {
    'text2img_model': 'stabilityai/stable-diffusion-xl-base-1.0',
    'img2anime_model': 'your_anime_model',
    'face_swap_model': 'your_face_swap_model'
}

# Cấu hình mặc định cho ảnh
IMAGE_CONFIG = {
    'default_width': 512,
    'default_height': 512,
    'max_width': 1024,
    'max_height': 1024
}

# Thông tin liên hệ
CONTACT_INFO = {
    'developer': 'Khôi Trần',
    'facebook': 'https://www.facebook.com/profile.php?id=100072140473156',
    'github': 'https://github.com/KtranH/KhoiTran-ProjectGradio1.git',
    'email': 'hoangkhoi230@gmail.com'
}