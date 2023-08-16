from flask import Flask,request,render_template,jsonify,json
from paddleocr import PaddleOCR,draw_ocr
import pytesseract as pytes
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import easyocr
import os
import re
import cv2
from PIL import Image
import requests
import json
ocr = PaddleOCR(use_angle_cls=True,lang='ch')
pytes.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path=r"C:\Users\VigneshSubramani\Documents\IMAGE\page_1.png"
result=ocr.ocr(image_path)
detected_text_list=[]
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        detected_text_list.append(line[1][0])
text = ' '.join(detected_text_list)
print(text)