import cv2
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import numpy as np
ocr = PaddleOCR(use_angle_cls=True,lang="en")
image_path = r"C:\Users\VigneshSubramani\Pictures\invoice image\imag2.png"
byte_format = cv2.imread(image_path)
print(byte_format)
result = ocr.ocr(image_path)
input_list =[]
for idx in range (len(result)):
    res = result[idx]
    for line in res:
        input_list.append(line[1][0])
    print(input_list)

