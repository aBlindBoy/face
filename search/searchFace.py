import MySQLdb
import numpy as np
import face_recognition
from flask import Flask, jsonify, request, redirect, json
from flask import Flask
from flask_cors import CORS

# 打开数据库连接
from entity.Image import Image

db = MySQLdb.connect("192.168.0.146", "root", "root", "face", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 判断图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/search', methods=['GET', 'POST'])
def upload_image():
    print("进来了-----------")
    # 检测图片是否上传成功
    if request.method == 'POST':
        print("进来了---")
        # 判断是否是文件
        print(request.files)
        if 'file' not in request.files:
            print("进来")
            return redirect(request.url)

        file = request.files['file']

        # 判断文件名是否为空
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # 图片上传成功，检测图片中的人脸
            return detect_faces_in_image(file)

    # 图片上传失败，输出以下html代码
    return ''


def detect_faces_in_image(file_stream):
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    # 为用户上传的图片进行编码
    face_encodings = face_recognition.face_encodings(img)
    # 查询出数据库全部人脸编码
    # face = [known_face_encoding]
    # print("原有参数类型", type(face), face)
    # print("上传文件的人脸类型", type(face_encodings[0]), face_encodings[0])
    # match_results = face_recognition.compare_faces(face, face_encodings[0])
    # for ma in match_results:
    #     print(ma)
    sql = "select f.face_id,f.image_id,f.face_encoding from face f"
    print("总共有", len(face_encodings), "张人脸")
    li = []
    imagePath = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # 遍历数据库人脸数据
        for index in range(len(face_encodings)):
            for re in results:
                # 将数组转成 list
                mysql_face = list(eval(re[2]))
                # fa = np.array(mysql_face, dtype=float)
                # print("类型", type(mysql_face), "====>>>", mysql_face)
                # upface = list(eval(face_encodings[0]))
                # print("上传人脸类型", type(face_encodings[index]), "=====>>>>", face_encodings[index])
                # 进行逐个比对 1.已知人脸 2.未知人脸
                match_results = face_recognition.compare_faces([mysql_face], face_encodings[index], 0.5)
                if match_results[0]:
                    # print(re[1], "===>>>比对成功")
                    li.append(re[1])
        print(li)
        li = list(set(li))
        print(li)
        for i in li:
            print(type(i))
            imagePathSql = "select i.image_id,i.image_path from image i where i.image_id = %s" % i
            cursor.execute(imagePathSql)
            fanhui = cursor.fetchall()
            for fa in fanhui:
                image = Image(fa[0], fa[1])
                # image = json.dumps(image.__dict__)
                imagePath.append(image.convert_to_dict)
    except IOError:
        print("不知道什么鬼?????  报错了")
    print(imagePath)
    return jsonify(imagePath)


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="127.0.0.1", port=10086, debug=False)
