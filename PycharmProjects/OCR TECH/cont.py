from flask import Flask,render_template,request
import cv2
import numpy as np
import pandas as pd
import easyocr
from  PIL import ImageDraw,Image
import requests
import re
import json
import base64
import matplotlib.pyplot as plt
image=cv2.imread("sample1.jpg")
ima= cv2.imread("sample1.jpg")
reader = easyocr.Reader(lang_list=["en"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
min_contour_area = 1000
table_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
result1 = reader.readtext(image)
for bbox in result1:
    pts = bbox[0]
    confidence = bbox[2]  # Get the confidence score of the detection
    cv2.rectangle(image, (int(pts[0][0]), int(pts[0][1])), (int(pts[2][0]), int(pts[2][1])), (0, 255, 0), 2)
    text = f'{confidence:.2f}'
    cv2.putText(image,text,(int(pts[0][0]), int(pts[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
plt.figure(figsize=(20,20))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('letters detection')
plt.show()
# Convert BGR image to base64
_, buffer = cv2.imencode('.png', image)
image_base64 = base64.b64encode(buffer).decode('utf-8')
res = reader.readtext(ima)
text = ''
for detection in res:
    text += detection[1] + ' '
print(text)