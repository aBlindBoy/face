import face_recognition
from flask import Flask, jsonify, request, redirect
from werkzeug.utils import secure_filename
import os
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("192.168.0.146", "root", "root", "face", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 判断图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        f = request.files['file']
        print(type(f))
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'F:\\upload\\image', secure_filename(f.filename))
        f.save(upload_path)

    if f and allowed_file(f.filename):
        # 图片上传成功，检测图片中的人脸
        return detect_faces_in_image(f)

    return ''


def detect_faces_in_image(file_stream):
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    # 为用户上传的图片中的人脸编码
    face_encodings = face_recognition.face_encodings(img)
    # print(face_encodings)
    # 文件名类型对象
    n = str(file_stream.filename)
    print(n)
    # 添加数据库
    sql_image = "INSERT INTO image (image_path)  VALUES ('%s')" % (n)
    print(sql_image)

    try:
        row = cursor.execute(sql_image)
        print("图片sql执行成功", row)
        image_id = cursor.lastrowid
        # 人脸编码添加到数据库
        list1 = []
        for face_encoding in face_encodings:
            # str1 = ''.join(face_encoding)
            s = ','.join('%s' % id for id in face_encoding)
            print(type(s), '===', s)
            list1.append((image_id, '[%s]' %s))
        print("参数 = ", str(list1))
        print("总共有", len(face_encodings), "张人脸")
        cursor.executemany('INSERT INTO face (image_id, face_encoding) values (%s,%s)', list1)
        db.commit()
        print('添加成功')
    except IOError:
         db.rollback()
         print('添加失败')
    # finally:
    #     db.close()
    result = {
        "code": "200",
        "msg": "上传成功"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=5004, debug=False)
