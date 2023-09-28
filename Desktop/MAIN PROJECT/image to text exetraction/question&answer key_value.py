from flask import Flask, request,send_file,json,jsonify,Response
from paddleocr import PaddleOCR,draw_ocr
import cv2
import numpy as np
import pypdfium2 as pdfium
import os
import io
from PIL import Image
import re
from transformers import (
    pipeline,set_seed,
    AutoModelForTokenClassification,
    AutoModelForQuestionAnswering,
    AutoTokenizer)
model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"
nlp = pipeline("question-answering",model=model_name,
                tokenizer=model_name)
ocr = PaddleOCR(use_angle_cls=True,lang='en')
image_path = r"C:\Users\VigneshSubramani\Pictures\invoice image\sample1.jpg"
result = ocr.ocr(image_path)
detected_text_list = []
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        detected_text_list.append(line[1][0])
text = ' '.join(detected_text_list)

def extract_mails(text):
    email_pattern = r"(?i)(?:email\s*:\s*)?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|\b[a-zA-Z0-9._%+-]+@gmail\.com\b)"
    mail_matches = re.findall(email_pattern, text)
    if mail_matches:
        return mail_matches
    else:
        return None
def extract_url(text):
    url_pattern = r'https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S*)?'
    url_matches = re.findall(url_pattern, text)
    if url_matches:
        return url_matches
    else:
        return None
def extract_mobile_number(text):
    combined_pattern = r'(\+91\s\d{10}|\b\d{10}\b|\b\d{6}-\d{4}\b|\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
    mobile_matches = re.findall(combined_pattern, text)
    if mobile_matches:
        return mobile_matches
    else:
        return None

def extract_dates(text):
    date_pattern = (
        r"(?i)\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|"
        r"\d{1,2}(?:st|nd|rd|th)? \w+ \d{2,4}|"
        r"\d{1,2} \w+ \d{2,4}|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{2,4}|"
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?) \d{1,2}, \d{4}|"
        r"[a-zA-Z]{3} \d{1,2}, \d{4}|"
        r"[a-zA-Z]{3} \d{1,2},\d{4})\b"
    )
    date_matches = re.findall(date_pattern,text)
    if date_matches:
        return date_matches
    else:
        return none

data = {}
def get_answer(question, text):
    qa_input = {'question': question,'context': text}
    res = nlp(qa_input)
    if res["answer"] and res["score"] >= 0.20:
        return res["answer"]
    return None
# make the pair on value
invoice_value= get_answer("what is the invoice# number?", text).split()
start_date_value= get_answer("what is the payment start date?", text)
end_date_value= get_answer("what is the payment due date?", text)
company_name_value = get_answer("what is the company name", text)
total_value = get_answer("what is the total amount?", text)
balance_due_value = get_answer("what is the payment balance due?", text)
sub_total_value= get_answer("what is the amount of subtotal?", text)
url_value= (extract_url(text))
mail_value = (extract_mails(text))
mobile_number_value = extract_mobile_number(text)
print(f"key:{invoice_value[0]}")
#print(str(invoice_value[0]))
