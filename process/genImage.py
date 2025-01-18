import os
import json
import time
import requests
import numpy as np

from PIL import Image
from datetime import datetime
from process.get_image import get_latest_image

URL = "http://127.0.0.1:8188/api/prompt"
INPUT_DIR = "D:\\ProjectPython\\gradioApp\\input"
ERROR = "D:\\ProjectPython\\gradioApp\\output"
OUTPUT_DIR = "D:\\ProjectPython\\gradioApp\\output"

cached_seed = 0
max_time = 5000
elapsed_time = 0

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

# Hàm tạo ảnh cho chức năng thay đổi biểu cảm khuôn mặt
def generate_image(input_image, rotate_pitch, rotate_yaw, rotate_roll, blink, eyebrow, wink, pupil_x, pupil_y, aaa, eee, woo, smile):
    error_image_path = os.path.join(ERROR, "error.jpg")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        with open("json/Live_Portait.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            prompt["17"]["inputs"]["image"] = os.path.join(INPUT_DIR, "InputImage_LivePortait_" + current_time + ".png")
            prompt["16"]["inputs"]["file_path"] = os.path.join(OUTPUT_DIR, "OutputImage_LivePortait_" + current_time + ".png")
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
            previous_image = get_latest_image(OUTPUT_DIR)
            if previous_image is None:
                return np.array(Image.open(error_image_path)) 
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image(OUTPUT_DIR)
                if latest_image is None:
                    return np.array(Image.open(error_image_path))
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
# Hàm tạo ảnh cho chức năng tạo ảnh sang anime
# Hàm tạo ảnh cho chức năng tạo ảnh sao chép khuôn mặt