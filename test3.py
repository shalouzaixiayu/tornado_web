# -*- coding :  utf-8 -*-
# @Time      :  2020/12/4  21:23
# @author    :  沙漏在下雨
# @Software  :  PyCharm
# @CSDN      :  https://me.csdn.net/qq_45906219
import tornado.web
import tornado.ioloop


class IndexHandle(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/reginster.html")

    def post(self):
        pass


app = tornado.web.Application(
    [(r'^/$', IndexHandle), ])

app.listen(8888)
print("http://127.0.0.1:8888")
tornado.ioloop.IOLoop.current().start()
