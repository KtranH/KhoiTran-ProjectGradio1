import os
import json
import time
import requests
import numpy as np
import gradio as gr

from PIL import Image
from datetime import datetime
from process.get_image import get_latest_image_LivePortait, get_latest_image_TextToImage, get_latest_image_ImgToImg

URL = "http://127.0.0.1:8188/api/prompt"
INPUT_DIR = "D:\\ProjectPython\\gradioApp\\input"
ERROR = "D:\\ProjectPython\\gradioApp\\output"
OUTPUT_DIR_LIVEPORTAIT = "D:\\ProjectPython\\gradioApp\\output\\livePortait"
OUTPUT_DIR_TEXT2IMAGE = "D:\\ProjectPython\\gradioApp\\output\\text2Img"
OUTPUT_DIR_IMG2IMG = "D:\\ProjectPython\\gradioApp\\output\\img2Img"
OUTPUT_DIR_INSTANTID = "D:\\ProjectPython\\gradioApp\\output\\instantID"

client_id = "null"
cached_seed = 0
max_time = 50000
elapsed_time = 0


def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

# Hàm tạo ảnh cho chức năng thay đổi biểu cảm khuôn mặt
def generate_image_LivePortait(input_image, rotate_pitch, rotate_yaw, rotate_roll, blink, eyebrow, wink, pupil_x, pupil_y, aaa, eee, woo, smile):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/Live_Portait.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            # Tùy chỉnh thông số tạo ảnh
            prompt["17"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_LivePortait_" + current_time + ".png")
            prompt["16"]["inputs"]["file_path"] = os.path.join(OUTPUT_DIR_LIVEPORTAIT, "OutputImage_LivePortait_" + current_time + ".png")
            prompt["14"]["inputs"]["rotate_pitch"] = rotate_pitch
            prompt["14"]["inputs"]["rotate_yaw"] = rotate_yaw
            prompt["14"]["inputs"]["rotate_roll"] = rotate_roll
            prompt["14"]["inputs"]["blink"] = blink
            prompt["14"]["inputs"]["eyebrow"] = eyebrow
            prompt["14"]["inputs"]["wink"] = wink
            prompt["14"]["inputs"]["pupil_x"] = pupil_x
            prompt["14"]["inputs"]["pupil_y"] = pupil_y
            prompt["14"]["inputs"]["aaa"] = aaa
            prompt["14"]["inputs"]["eee"] = eee
            prompt["14"]["inputs"]["woo"] = woo
            prompt["14"]["inputs"]["smile"] = smile

            # Xử lý ảnh tải lên
            image = Image.fromarray(input_image)
            min_side = min(image.size)
            scale_factor = 512 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)
            resized_image.save(os.path.join(INPUT_DIR, "InputImage_LivePortait_" + current_time + ".png"))

            # Bắt đầu quá trình tạo ảnh
            previous_image = get_latest_image_LivePortait(OUTPUT_DIR_LIVEPORTAIT)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image_LivePortait(OUTPUT_DIR_LIVEPORTAIT)
                if latest_image != previous_image:
                    return np.array(Image.open(latest_image))
                
                elapsed_time += 10
                time.sleep(1)

                if elapsed_time >= max_time:
                    return np.array(Image.open(error_image_path))
                
    except Exception as e:
        print("An error occurred:", str(e))
        return np.array(Image.open(error_image_path))

# Hàm tạo ảnh cho chức năng tạo ảnh bằng văn bản
def generate_image_TextToImage(seed, text, width, height, model):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/Text_2_Img.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            # Tùy chỉnh thông số tạo ảnh
            prompt["12"]["inputs"]["noise_seed"] = seed
            prompt["22"]["inputs"]["text_a"] = text
            prompt["11"]["inputs"]["width"] = width
            prompt["11"]["inputs"]["height"] = height
            prompt["29"]["inputs"]["file_path"] = os.path.join(OUTPUT_DIR_TEXT2IMAGE, "OutputImage_TextToImage_" + current_time + ".png")

            # Căn chỉnh phong cách tạo ảnh
            if model == "Chân thực":
                prompt["22"]["inputs"]["text_b"] = "realistic"
            elif model == "Hoạt hình":
                prompt["22"]["inputs"]["text_b"] = "anime"
            else:
                prompt["22"]["inputs"]["text_b"] = "3D cute"

            # Bắt đầu quá trình tạo ảnh
            previous_image = get_latest_image_TextToImage(OUTPUT_DIR_TEXT2IMAGE)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image_TextToImage(OUTPUT_DIR_TEXT2IMAGE)
                if latest_image != previous_image:
                    return np.array(Image.open(latest_image))
                
                elapsed_time += 10
                time.sleep(1)

                if elapsed_time >= max_time:
                    return np.array(Image.open(error_image_path))
                
    except Exception as e:
        print("An error occurred:", str(e))
        return np.array(Image.open(error_image_path))
# Hàm tạo ảnh cho chức năng tạo ảnh sang chibi
def generate_image_ImgToImg(seed, input_image, width, height):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/Img_2_Img.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            # Tùy chỉnh thông số tạo ảnh
            prompt["8"]["inputs"]["seed"] = seed
            prompt["11"]["inputs"]["width"] = width
            prompt["11"]["inputs"]["height"] = height
            prompt["33"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_ImgToImg_" + current_time + ".png")
            prompt["34"]["inputs"]["file_path"] = os.path.join(OUTPUT_DIR_IMG2IMG, "OutputImage_ImgToImg_" + current_time + ".png")

            # Xử lý ảnh tải lên
            image = Image.fromarray(input_image)
            min_side = min(image.size)
            scale_factor = 512 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)
            resized_image.save(os.path.join(INPUT_DIR, "InputImage_ImgToImg_" + current_time + ".png"))

            # Bắt đầu quá trình tạo ảnh
            previous_image = get_latest_image_ImgToImg(OUTPUT_DIR_IMG2IMG)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image_ImgToImg(OUTPUT_DIR_IMG2IMG)
                if latest_image != previous_image:
                    return np.array(Image.open(latest_image))
                
                elapsed_time += 10
                time.sleep(1)

                if elapsed_time >= max_time:
                    gr.Error("Đã xảy ra lỗi! Vui lòng thử lại.", duration=3)
                    return np.array(Image.open(error_image_path))
                
    except Exception as e:
        print("An error occurred:", str(e))
        gr.Error("Đã xảy ra lỗi! Vui lòng thử lại.", duration=3)
        return np.array(Image.open(error_image_path))
# Hàm tạo ảnh cho chức năng tạo ảnh sao chép khuôn mặt