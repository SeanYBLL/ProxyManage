"""
api.py模块身处db.py和Flask接口之间，发挥通过python语言调用Flask服务的作用。而可用的ip代理就通过Flask服务对应的网址页面呈现出来，方便用户读取和使用。
"""


import json
from flask import Flask, g

from config import API_PORT
from db import RedisClient




def get_redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis
app = Flask(__name__)

@app.route('/')
def index():
    html = """
        <h1 style='color:green'>欢迎来到代理池监控维护器</h1>
        <hr/>
        <ul>
            <li><a href="/get_proxy/">代理IP的API地址</a></li>
            <li><a href="/count/">IP池代理IP的个数</a></li>
        </ul>
         
    """
    return html

@app.route('/get_proxy/')
def get_proxy():
    r= RedisClient()
    proxy =r.random()
    return proxy
@app.route('/count')
def count():
    r =RedisClient()
    return str(r.count())


# @app.route('/get_proxy/')
# def get_proxy():
#     """
#      Get a proxy
#     :return:随机代理
#     """
#     try:
#         conn = get_redis_conn()
#         return conn.random()
#     except Exception as e:
#         return e
#
# @app.route('/count/')
# def get_counts():
#     """
#     Get the count of proxies
#     :return: 代理池总量
#     """
#     conn = get_redis_conn()
#     return str(conn.count())
#
#
# @app.route('/many_proxy/')
# @app.route('/many_proxy/<int:count>/')
# def get_many(count=5):
#     """
#     Get the count of proxies
#     :return: 代理池总量
#     """
#     conn = get_redis_conn()
#     proxies = conn.batch(count-1)
#     return json.dumps(proxies)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port =6666)
