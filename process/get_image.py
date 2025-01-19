import os
### def get_latest_image(folder):
###    files = os.listdir(folder)
###    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
###    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
###    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
###    return latest_image

### def get_latest_image(folder):
###    try:
###        files = os.listdir(folder)
###        if not files:
###            return None
###        latest_image = os.path.join(folder, max(files))
###        return latest_image
###        
###    except Exception as e:
###        print(f"Lỗi khi lấy ảnh: {e}")
###        return None

def get_latest_image(folder):
    try:
        # Lấy các file có format đúng
        files = [f for f in os.listdir(folder) 
                if f.startswith('OutputImage_LivePortait_') and f.endswith('.png')]
        if not files:
            return None
        
        # Lấy file có timestamp lớn nhất
        latest_image = os.path.join(folder, max(files))
        return latest_image
        
    except Exception as e:
        print(f"Lỗi khi lấy ảnh: {e}")
        return None