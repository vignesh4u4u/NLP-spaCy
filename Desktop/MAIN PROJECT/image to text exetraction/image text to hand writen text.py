from paddleocr import PaddleOCR
import pywhatkit as kit
from PIL import Image
import cv2
image_path = r"C:\Users\VigneshSubramani\Pictures\invoice image\imag2.png"
ocr = PaddleOCR(use_angle_cls=True, lang="en")
result = ocr.ocr(image_path)
extracted_text = []
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        extracted_text.append(line[1][0])
    text=" ".join(extracted_text)
#kit.text_to_handwriting(text)