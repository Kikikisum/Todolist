from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
HOSTNAME = ""
PORT = 3306
USERNAME = ""
PASSWORD = ""
DATABASE = ""
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
db = SQLAlchemy(app)


@app.route('/add', methods=["POST"])
def add():  # put application's code here
    """
    增加一个事项
    :return:
    """
    try:
        id = request.json.get("id").strip()
        title = request.json.get("title").strip()
        content = request.json.get("content", "").strip()
        state = request.json.get("state", "").strip()
        create_time = int(time.time())
        end_time = request.json.get("end_time", "").strip()
        timeArray = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        end_time = int(time.mktime(timeArray))
        sql_ins = f"""INSERT INTO event VALUES ('{id}','{title}','{content}','{state}','{create_time}','{end_time}')"""
        with db.engine.connect() as conn:
            data = conn.execute(sql_ins)
        data = data.fetchall()[0]
        return jsonify(
                {"code": 200, "msg": "success", "id": data[0], "title": data[1], "content": data[2], "state": data[3],
                 "create_time": data[4], "end_time": data[5]})
    except Exception as e:
        return jsonify({"code": 200, "msg": e})


@app.route("/accomplish", methods=["POST"])
def accomplish():
    """
    修改某一个事项为完成
    :return:
    """
    try:
        id = request.json.get("id").strip()
        sql_up = f"""UPDATE event SET state ='完成' WHERE id ='{id}'"""
        with db.engine.connect() as conn:
            conn.execute(sql_up)
        return jsonify({"code": 200, "msg": "success"})
    except Exception as e:
        return jsonify({"code": 200, "msg": e})


@app.route("/unfinished", methods="POST")
def unfinished():
    """
        修改某一个事项为待办
        :return:
        """
    try:
        id = request.json.get("id").strip()
        sql_up = f"""UPDATE event SET state='待办' WHERE id='{id}'"""
        with db.engine.connect() as conn:
            data = conn.execute(sql_up)
        data = data.fetchall()[0]
        return jsonify(
            {"code": 200, "msg": "success", "id": data[0], "title": data[1], "content": data[2], "state": data[3],
             "create_time": data[4], "end_time": data[5]})
    except Exception as e:
        return jsonify({"code": 200, "msg": e})

@app.route("/query/finish",methods=['POST'])
def query_finish():
    """
            查找所有已完成/所有待办/所有事项
            :return:
            """
    sql_se = f"""SELECT * FROM event WHERE state ='完成'"""
    with db.engine.connect() as conn:
        data = conn.execute(sql_se)
    try:
        data = conn.fetchall()
        return jsonify({"code": 200, "meg": "success", "data": "data"})
    except:
        return jsonify({"code": 200, "meg": "没有已完成事项"})

@app.route("/query/unfinish",methods = ['POST'])
def query_unfinish():
    sql_se = f"""SELECT * FROM event WHERE state ='待办'"""
    with db.engine.connect() as conn:
        data = conn.execute(sql_se)
    try:
        data = conn.fetchall()
        return jsonify({"code": 200, "meg": "success", "data": "data"})

    except:
        return jsonify({"code": 200, "meg": "没有待办事项"})


@app.route("/query/all")
def query_all():
    sql_se = f"""SELECT * FROM event """
    with db.engine.connect() as conn:
        data = conn.execute(sql_se)
    try:
        data = conn.fetchall()
        return jsonify({"code": 200, "meg": "success", "data": "data"})
    except:
        return jsonify({"code": 200, "meg": "没有事项"})


@app.route("/query/title")
def query_title():
    """
        查找关键词
        :return:
        """
    title = request.json.get("title").strip()
    sql_se = f"""SELECT * FROM event WHERE title ='{title}'"""
    with db.engine.connect() as conn:
        data = conn.execute(sql_se)
    try:
        data = data.fetchall()[0]
        return jsonify(
            {"code": 200, "msg": "success", "id": data[0], "title": data[1], "content": data[2], "state": data[3],
             "create_time": data[4], "end_time": data[5]})
    except:
        return jsonify({"code": 200, "msg": "没有此项"})


@app.route("/query/id", methods=['POST'])
def query_id():
    """
    查找id
    :return:
    """
    # request.json.get("username")即从发送的json格式的请求参数中获取id的值
    id = request.json.get("id").strip()
    sql_se = f"""SELECT * FROM event WHERE id='{id}'"""
    with db.engine.connect() as conn:
        data = conn.execute(sql_se)
    try:
        data = data.fetchall()[0]
        return jsonify(
            {"code": 200, "msg": "success", "id": data[0], "title": data[1], "content": data[2], "state": data[3],
             "create_time": data[4], "end_time": data[5]})
    except:
        return jsonify({"code": 200, "msg": "没有此项"})


@app.route("/delete", methods=['POST'])
def delete():
    """
    删除
    :return:
    """
    try:
        id = request.json.get("id").strip()
        sql_de = f"""DELETE FROM event WHERE id='{id}'"""
        with db.engine.connect() as conn:
            data = conn.execute(sql_de)
        data = data.fetchall()[0]
        return jsonify(
            {"code": 200, "msg": "success", "id": data[0], "title": data[1], "content": data[2], "state": data[3],
             "create_time": data[4], "end_time": data[5]})
    except Exception as e:
        return jsonify({"code": 200, "msg": e})


if __name__ == '__main__':
    app.run()
