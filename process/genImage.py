import os
import json
import time
import requests
import numpy as np
from PIL import Image

URL = "http://127.0.0.1:8188/api/prompt"
INPUT_DIR = "D:\\ProjectPython\\gradioApp\\input"
ERROR = "D:\\ProjectPython\\gradioApp\\input\\error"
OUTPUT_DIR = "D:\\ProjectPython\\gradioApp\\output"

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)
def generate_image(input_image, seed_input):
    error_image_path = os.path.join(ERROR, "error.jpg")
    try:
        with open("Model.json", "r", encoding="utf-8") as file_json:
            prompt = json.load(file_json)

            prompt["130"]["inputs"]["image"] = os.path.join(INPUT_DIR, "Test_api.png")
            prompt["129"]["inputs"]["file_path"] = OUTPUT_DIR
            prompt["67"]["inputs"]["seed"] = seed_input
            
            image = Image.fromarray(input_image)
            min_side = min(image.size)
            scale_factor = 512 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)

            resized_image.save(os.path.join(INPUT_DIR, "Test_api.png"))

            previous_image = get_latest_image(OUTPUT_DIR)
            start_queue(prompt)

            global elapsed_time
            while True:
                latest_image = get_latest_image(OUTPUT_DIR)
                if latest_image != previous_image:
                    return np.array(Image.open(latest_image))
                
                elapsed_time += 10
                time.sleep(2)

                if elapsed_time >= max_time:
                    return np.array(Image.open(error_image_path))
                
    except Exception as e:
        print("An error occurred:", str(e))
        return np.array(Image.open(error_image_path))