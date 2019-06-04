# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

import face_recognition

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'F:\\uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # 文件上传保存路径
        f.save(upload_path)

        # 判断是否是图片 是图片就进行识别
        if f and allowed_file(f.filename):
            return detect_faces_in_image(f)


    result = {
        "code": "500",
        "msg": "上传失败"
    }
    return jsonify(result)

def detect_faces_in_image(file_stream):
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    # 为用户上传的人脸编码
    upload_face_encoding = face_recognition.face_encodings(img)

    for u in upload_face_encoding:
        print(u)

    # 将编码保存到数据库中


    result = {
      "code": "200",
      "msg": "上传成功"
    }
    return jsonify(result)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
