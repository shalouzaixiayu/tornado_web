# -*- coding :  utf-8 -*-
# @Time      :  2020/12/2  10:03
# @author    :  沙漏在下雨
# @Software  :  PyCharm
# @CSDN      :  https://me.csdn.net/qq_45906219
"""
关于 tornado 的练习课程
"""
from typing import Optional, Awaitable, Union, Any

import tornado.web
import tornado.ioloop
import os
import time
import pymysql
from sss import pwd

FILE_PATH = 'file/'


class IndexHandler(tornado.web.RequestHandler):
    """简单的get 和 post  方式 进行验证"""

    def get(self, *args, **kwargs):
        self.render('templates/index.html')

    def post(self, *args, **kwargs):
        name = self.get_argument("name")
        img = self.request.files.get("img")
        # 循环下载图片
        for im in img:
            body = im.get("body")
            filename = im.get("filename")
            content_type = im.get("content_type")
            print(content_type)
            # 写入文件中
            self.set_header("Content-Type", content_type)
            with open(os.path.join(FILE_PATH, filename), 'wb') as fw:
                fw.write(body)
            print(name)
            self.write(body)


class LoginHandler(tornado.web.RequestHandler):
    """
    用来限制 ip 登陆 和 useragent 的登陆限制
    """

    ug_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"]
    # ip 池
    ip_count = {}

    def get(self):
        print(self.ip_count)
        # 先验证请求头
        ug = self.request.headers.get("user-agent")
        if ug not in self.ug_list:
            self.send_error(403)

        # 再验证 ip
        current_ip = self.request.remote_ip
        #  在一定时间内， 不能允许重复登陆 max 次
        if current_ip not in self.ip_count.keys():
            self.ip_count[current_ip] = {"count": 1, "time_a": int(time.time())}
        else:
            self.ip_count[current_ip]["count"] += 1
            self.ip_count[current_ip]["time_a"] = int(time.time()) - self.ip_count[current_ip]["time_a"]
        # 进行判断
        if self.ip_count[current_ip]["count"] >= 20 and self.ip_count[current_ip]["time_a"] <= 30:
            self.send_error(403)
        else:
            pass


def _ConnectDB():
    return pymysql.connect(user="root", host="127.0.0.1", db="tornado", passwd=pwd,
                           port=3306)


class SaveToMysql(tornado.web.RequestHandler):
    # 用来绑定数据库， 进行数据库的字段提交
    def initialize(self, db):
        self.db = db

    def get(self):
        return self.render("templates/reginster.html")

    def prepare(self) -> Optional[Awaitable[None]]:
        return super().prepare()

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        super().write_error(status_code, **kwargs)

    def post(self):
        name = self.get_argument("username")
        age = self.get_argument("age")
        try:
            cursor = self.db.cursor()
            cursor.execute(f"insert into t_username values(0 ,'{name}', '{age}', now());")
            self.db.commit()
            self.redirect("http://www.baidu.com")
        except Exception as e:
            self.db.rollback()
            self.redirect('/reginster.html')


if __name__ == '__main__':
    setting = {"debug": True}
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/login.html", LoginHandler),
        (r'/reginster.html', SaveToMysql, {"db": _ConnectDB()}),
    ], **setting)
    # 绑定一个监听端口
    app.listen(8888)
    # 启动web程序， 开始监听端口连接
    print("http://127.0.0.1:8888/")
    tornado.ioloop.IOLoop.current().start()
