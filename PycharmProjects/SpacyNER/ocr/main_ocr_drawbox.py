import os
import io
import numpy as np
import io
import shutil

import cv2
from PIL import Image
import pypdfium2 as pdfium
from flask import request,send_file,json,jsonify,Response
from paddleocr import PaddleOCR,draw_ocr
class OcrMethodCoordinates:
    ocr = None
    def __init__(self):
        if OcrMethodCoordinates.ocr is None:
            OcrMethodCoordinates.ocr = PaddleOCR(use_angle_cls=True,lang='en')

    def coordinates(self, file):
        print("Converting file: ", file)
        file_end = file.filename.endswith(".pdf")

        if file_end == True:
            file_path = io.BytesIO(file.read())
            pdf = pdfium.PdfDocument(file_path)
            n_pages = len(pdf)
            image_path_list = []
            for page_number in range(n_pages):
                page = pdf.get_page(page_number)
                pil_image = page.render(scale=3).to_pil()
                image_path = f"image_{page_number + 1}.png"
                pil_image.save(image_path)
                image_path_list.append(image_path)
            processed_images = []
            for image_path in image_path_list:
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                result = OcrMethodCoordinates.ocr.ocr(gray)
                boxes = [line[0] for line in result[0]]
                txts = [line[1][0] for line in result[0]]
                scores = [line[1][1] for line in result[0]]
                font_path = "latin.ttf"
                im_show = draw_ocr(image, boxes, font_path=font_path)
                pil_im_show = Image.fromarray(im_show)
                image_buffer = io.BytesIO()
                pil_im_show.save(image_buffer, format="PNG")
                image_buffer.seek(0)
                processed_images.append(image_buffer)
            pdf.close()
            os.remove(image_path)
            print("temporary image path library removed")
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
                    detected_text_and_boxes.append({
                        'text': text,
                        'x1,y1': [x1, y1],
                        'x2,y2': [x2, y2],
                        'x3,y3': [x3, y3],
                        'x4,y4': [x4, y4]
                    })
            res_image = send_file(processed_images[0], mimetype='image/png')
            output_json = json.dumps(detected_text_and_boxes, indent=2, separators=(',', ':'))
            return res_image
        else:
            image_data = file.read()
            gray = cv2.cvtColor(cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR),
                                cv2.COLOR_BGR2GRAY)
            result = OcrMethodCoordinates.ocr.ocr(gray)
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            boxes = [line[0] for line in result[0]]
            txts = [line[1][0] for line in result[0]]
            scores = [line[1][1] for line in result[0]]
            font_path = "latin.ttf"
            im_show = draw_ocr(image, boxes, font_path=font_path)
            pil_im_show = Image.fromarray(im_show)
            image_buffer = io.BytesIO()
            pil_im_show.save(image_buffer, format="PNG")
            image_buffer.seek(0)
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
                    detected_text_and_boxes.append({
                        'text': text,
                        'x1,y1': [x1, y1],
                        'x2,y2': [x2, y2],
                        'x3,y3': [x3, y3],
                        'x4,y4': [x4, y4]
                    })
            res_image = send_file(image_buffer, mimetype='image/png')
            output_json = json.dumps(detected_text_and_boxes, indent=2, separators=(',', ':'))
            return res_image



