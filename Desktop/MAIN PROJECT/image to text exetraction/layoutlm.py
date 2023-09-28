from paddleocr import PaddleOCR,draw_ocr
from flask import Flask,request,jsonify,json
ocr = PaddleOCR(use_angle_cls=True,lang ="en")
CONTEXT_PATH = "/ml-service"
flask_app = Flask(__name__)

@flask_app.route(CONTEXT_PATH + "/image_text/v1/extract", methods=["POST"])
def image_text_extraction():
    if request.method == "POST":
        file = request.files["file"]
        image_data = file.read()
        result = ocr.ocr(image_data)
        extracted_text = ""
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                extracted_text += line[1][0]
        return jsonify({"extracted_text": extracted_text})

if __name__=="__main__":
    flask_app.run(debug=True,host="0.0.0.0",port=5008)
