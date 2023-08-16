from flask import  Flask,request,render_template,jsonify,json
from pdfminer.high_level import extract_text,extract_pages,extract_text_to_fp
from camelot import read_pdf
from tabula import read_pdf
import numpy as np
import scipy as scy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import json
from PIL import Image,ImageDraw
import os
import re
app=Flask(__name__)
@app.route("/ml-service/pdfocr/v1/ping",methods=["GET"])
def home():
    if request.method == 'GET':
        return "pong"
@app.route("/ml-service/pdfocr", methods=["POST"])
def extract_text_information_pdf():
    if request.method == 'POST':
        file = request.files["file"]
        fields_input = request.form["fields"]
        fields = json.loads(fields_input)
        file_path = "temp.pdf"
        file.save(file_path)
        with open(file_path,'rb') as f:
            text = extract_text(f)
        data = {}
        for field in fields:
            key = field.get("key")
            pattern = field.get("pattern")
            repeatable = field.get("repeatable", True)
            if pattern:
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                if matches:
                    if repeatable:
                        data[key] = matches
                    else:
                        data[key] = matches[0]
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "No matching data found"})
        os.remove(file_path)
    #return render_template("che.html", **locals())
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)