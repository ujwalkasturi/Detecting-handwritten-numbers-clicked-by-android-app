import os
import cv2
from flask import Flask, request
from mnistModel import detect_num as detect
import numpy as np

app = Flask(__name__)

absolutePath = os.path.dirname(__file__)
relativePath = os.path.join(absolutePath, 'categories/')

@app.route('/', methods=['POST'])
def upload():
    


    file1 = request.files['image']
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    num = detect(img)
    UPLOAD_FOLDER = os.path.join(relativePath, str(num))
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    path = os.path.join(UPLOAD_FOLDER, file1.filename)
   
    file1.seek(0)
    file1.save(path)

    return (str(num))

    


if __name__ == '__main__':
    app.run(host='0.0.0.0')