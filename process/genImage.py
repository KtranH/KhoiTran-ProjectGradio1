import os
import json
import time
import requests
import numpy as np
import gradio as gr

from PIL import Image
from datetime import datetime
from process.get_image import get_latest_image_LivePortait, get_latest_image_TextToImage, get_latest_image_ImgToImg, get_latest_image_InstantID, get_latest_image_InstantID_hyperlora

URL = "http://127.0.0.1:8188/api/prompt"
INPUT_DIR = "D:\\ProjectPython\\gradioApp\\input"
ERROR = "D:\\ProjectPython\\gradioApp\\output"
OUTPUT_DIR_LIVEPORTAIT = "D:\\ProjectPython\\gradioApp\\output\\livePortait"
OUTPUT_DIR_TEXT2IMAGE = "D:\\ProjectPython\\gradioApp\\output\\text2Img"
OUTPUT_DIR_IMG2IMG = "D:\\ProjectPython\\gradioApp\\output\\img2Img"
OUTPUT_DIR_INSTANTID = "D:\\ProjectPython\\gradioApp\\output\\instantID"
OUTPUT_DIR_INSTANTID_HYPERLORA = "D:\\ProjectPython\\gradioApp\\output\\instantID_hyperlora"

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
            prompt["49"]["inputs"]["custom_path"] = OUTPUT_DIR_TEXT2IMAGE
            prompt["49"]["inputs"]["filename_prefix"] = "OutputImage_TextToImage_" + current_time

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
def generate_instant_id(seed, input_image, prompt_text, width, height, weight_instantid):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/Instant_ID.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            # Tùy chỉnh thông số tạo ảnh
            prompt["357"]["inputs"]["seed"] = seed
            prompt["345"]["inputs"]["width"] = width
            prompt["345"]["inputs"]["height"] = height
            prompt["383"]["inputs"]["text_a"] = prompt_text
            prompt["336"]["inputs"]["weight"] = weight_instantid
            prompt["416"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_InstantID_" + current_time + ".png")
            prompt["417"]["inputs"]["file_path"] = os.path.join(OUTPUT_DIR_INSTANTID, "OutputImage_InstantID_" + current_time + ".png")

            # Xử lý ảnh tải lên
            image = Image.fromarray(input_image)
            min_side = min(image.size)
            scale_factor = 512 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)
            resized_image.save(os.path.join(INPUT_DIR, "InputImage_InstantID_" + current_time + ".png"))

            # Bắt đầu quá trình tạo ảnh
            previous_image = get_latest_image_InstantID(OUTPUT_DIR_INSTANTID)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image_InstantID(OUTPUT_DIR_INSTANTID)
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

# Hàm tạo ảnh cho chức năng tạo ảnh sao chép khuôn mặt (HyperLora)
def generate_instant_id_hyperlora(seed, input_image, input_image2, prompt_text, width, height, hyper_lora):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/HyperLora_1.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            # Tùy chỉnh thông số tạo ảnh
            prompt["58"]["inputs"]["noise_seed"] = seed
            prompt["11"]["inputs"]["width"] = width
            prompt["11"]["inputs"]["height"] = height
            prompt["22"]["inputs"]["text_a"] = prompt_text
            prompt["40"]["inputs"]["weight"] = hyper_lora
            prompt["41"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_InstantID_hyperlora_1" + current_time + ".png")
            prompt["71"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_InstantID_hyperlora_2" + current_time + ".png")
            prompt["73"]["inputs"]["custom_path"] = os.path.join(OUTPUT_DIR_INSTANTID_HYPERLORA)
            prompt["73"]["inputs"]["filename_prefix"] = "OutputImage_InstantID_hyperlora_" + current_time

            # Xử lý ảnh tải lên
            image = Image.fromarray(input_image)
            min_side = min(image.size)
            scale_factor = 512 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)
            resized_image.save(os.path.join(INPUT_DIR, "InputImage_InstantID_hyperlora_1" + current_time + ".png"))

            # Xử lý ảnh tải lên
            image2 = Image.fromarray(input_image2)
            min_side = min(image2.size)
            scale_factor = 512 / min_side
            new_size = (round(image2.size[0] * scale_factor), round(image2.size[1] * scale_factor))
            resized_image2 = image2.resize(new_size)
            resized_image2.save(os.path.join(INPUT_DIR, "InputImage_InstantID_hyperlora_2" + current_time + ".png"))

            # Bắt đầu quá trình tạo ảnh
            previous_image = get_latest_image_InstantID_hyperlora(OUTPUT_DIR_INSTANTID_HYPERLORA)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image_InstantID_hyperlora(OUTPUT_DIR_INSTANTID_HYPERLORA)
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