import os
from pathlib import Path

def remove_extra_images(folder_path, max_files=10, exclude_file="error.jpg"):
    # Kiểm tra đường dẫn folder
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"Folder không tồn tại: {folder}")
        return

    # Lọc danh sách file ảnh trong folder (ngoại trừ file exclude_file)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
    image_files = [file for file in folder.iterdir() 
                   if file.suffix.lower() in image_extensions and file.name != exclude_file]

    # Kiểm tra số lượng file ảnh
    if len(image_files) > max_files:
        print(f"Folder '{folder_path}' có {len(image_files)} ảnh, vượt quá {max_files}. Bắt đầu xóa...")
        
        # Sắp xếp file theo thời gian sửa đổi (cũ nhất trước)
        image_files.sort(key=lambda x: x.stat().st_mtime)
        
        # Xóa các file thừa, giữ lại max_files và exclude_file
        files_to_delete = image_files[:len(image_files) - max_files]
        for file in files_to_delete:
            try:
                file.unlink()
                print(f"Đã xóa: {file}")
            except Exception as e:
                print(f"Lỗi khi xóa file {file}: {e}")
    else:
        print(f"Folder '{folder_path}' có số lượng ảnh hợp lệ: {len(image_files)}.")


def check_and_clean_folders(folder1, folder2, max_files=10, exclude_file="error.jpg"):
    print("Kiểm tra folder 1...")
    remove_extra_images(folder1, max_files, exclude_file)
    print("Kiểm tra folder 2...")
    remove_extra_images(folder2, max_files, exclude_file)


# Sử dụng hàm
folder1 = "D:\\ProjectPython\\gradioApp\\input"  # Thay bằng đường dẫn folder 1
folder2 = "D:\\ProjectPython\\gradioApp\\output"  # Thay bằng đường dẫn folder 2
check_and_clean_folders(folder1, folder2)
