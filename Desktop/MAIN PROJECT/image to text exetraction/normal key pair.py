from flask import Flask, request,send_file,json,jsonify,Response
from paddleocr import PaddleOCR,draw_ocr
import cv2
import numpy as np
import pypdfium2 as pdfium
import os
import io
from PIL import Image
ocr = PaddleOCR(use_angle_cls=True,lang='en')
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
        gray = cv2.cvtColor(cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY)
        result = ocr.ocr(gray)
        detected_text_and_boxes = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                text = line[1][0]
                points = line[0]
                x1, y1 = points[0]
                x2, y2 = points[1]
                x3, y3 = points[2]
                x4, y4 = points[3]
                detected_text_and_boxes.append(text)
        modified_detected_text = []
        for idx, text in enumerate(detected_text_and_boxes):
            if text.endswith(":"):
                if idx < len(detected_text_and_boxes) - 1:
                    modified_text = text + " " + detected_text_and_boxes[idx + 1]
                    modified_detected_text.append(modified_text)
            else:
                modified_detected_text.append(text)
        #print(modified_detected_text)
        #print(detected_text_and_boxes)
        key_value_pairs = {}
        current_key = None
        for item in modified_detected_text:
            if ':' in item:
                current_key, current_value = item.split(':', 1)
                key_value_pairs[current_key] = current_value
        return key_value_pairs
if __name__ == "__main__":
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
