from flask import Flask,request,render_template,send_file,Response,jsonify,json
import easyocr
from huggingface_hub import list_datasets
dataset_id = [dataset.id for dataset in list_datasets()]
reader = easyocr.Reader(lang_list=['en'],gpu=False)

imag_path = r"C:\Users\VigneshSubramani\Pictures\invoice image\imag2.png"
result = reader.readtext(imag_path)
#print(result)
for i in result:
    text = i[1]
    #print(text)