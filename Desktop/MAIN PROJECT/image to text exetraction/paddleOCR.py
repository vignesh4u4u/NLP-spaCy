import cv2
import numpy as np
from flask import Flask,Response,request,jsonify
from PIL import Image,ImageDraw
from paddleocr import PaddleOCR,draw_ocr

ocr = PaddleOCR(use_angle_cls=True,lang="en")
CONTEXT_PATH = "/ml-service"
flask_app = Flask(__name__)
@flask_app.route(CONTEXT_PATH + "/health/v1/ping", methods=["GET"])
def health_check():
    return "pong"
@flask_app.route(CONTEXT_PATH + "/image_text/v1/extract", methods=["POST"])
def image_text_extraction():
    if request.method == "POST":
        file = request.files["file"]
        image_data = file.read()
        result = ocr.ocr(image_data)
        text_list =[]
        for idx in range (len(result)):
            res = result[idx]
            for line in res:
               text_list.append(line[1][0])
        text = " ".join(text_list)

        modified_detected_text = []
        for idx, text in enumerate(text_list):
            if text.endswith(":"):
                if idx < len(text_list) - 1:
                    modified_text = text + " " + text_list[idx + 1]
                    modified_detected_text.append(modified_text)
            else:
                modified_detected_text.append(text)
        key_value_pairs = {}
        current_key = None
        for item in modified_detected_text:
            if ':' in item:
                current_key, current_value = item.split(':', 1)
                key_value_pairs[current_key] = current_value
        return key_value_pairs

if __name__=="__main__":
    flask_app.run(debug=True,host="0.0.0.0",port=5008)