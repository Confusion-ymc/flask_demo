import hashlib
import time

from flask import Flask, request
from flask import jsonify
from flask_cors import cross_origin
from utils import jwt_decode, jwt_encode, send_email, validateEmail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # 创建一个Flask app对象

db = SQLAlchemy(app)
DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "4399"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "chinamobile"
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI


class User(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    job_id = db.Column(db.String(50), unique=True)  # id 整型，主键，自增，唯一
    score = db.Column(db.Integer, default=0)  # 年龄 整型，默认为20

    __tablename__ = 'user'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    # def __init__(self, job_id, score):  # 初始化方法，可以对对象进行创建
    #     self.s_name = name
    #     self.s_age = age


db.create_all()


@app.route('/cost_score', methods=['POST'])
def cost_score():
    # request.POST['']
    if request.method == 'POST':
        token = request.json['data']
        data = jwt_decode(token)
        if not data:
            return jsonify({'status': 500, 'score': 0})
        job_id = data['job_id']
        user = User.query.filter(User.job_id == job_id).first()
        if not user:
            user = User(job_id=job_id)
            db.session.add(user)
            db.session.commit()
            res_data = {'status': 200, 'score': user.score}
        else:
            cost = data['cost']
            if user.score > 0:
                user.score -= cost
                db.session.commit()
            res_data = {'status': 200, 'score': user.score}
        return jsonify({'data': jwt_encode(res_data)})

    # jwt_token = jwt_encode('1008611', 1)


@app.route('/<int:time_stamp>')
def hello_world(time_stamp):
    code = request.args.get("code")
    if int(time.time()) - time_stamp > 60:
        return '0'
    data = '1' + str(time_stamp) + '2'
    md5 = hashlib.md5()  # 应用MD5算法
    md5.update(data.encode('utf-8'))
    crypto = md5.hexdigest()
    if crypto != code:
        return '0'
    return '1'


@app.route('/send_email', methods=["POST"])
@cross_origin()
def get_tasks():
    if request.method == 'POST':
        from_user = request.form['email']
        if not validateEmail(from_user):
            return jsonify({'status': 500, 'msg': '发送失败,邮箱地址不合法'}), 500
        title = request.form['title']
        msg = request.form['msg']
        try:
            email_body = '''
            发送者：{from_user}
            标题：{title}
            内容：{msg}
            '''.format(title=title, msg=msg, from_user=from_user)
            send_email(['1836336521@qq.com'], title, email_body)
            return jsonify({'status': 200, 'msg': '发送成功'}), 200
        except Exception as e:
            print(e)
            return jsonify({'status': 500, 'msg': '发送失败'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=83)
