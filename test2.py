# -*- coding :  utf-8 -*-
# @Time      :  2020/12/4  20:42
# @author    :  沙漏在下雨
# @Software  :  PyCharm
# @CSDN      :  https://me.csdn.net/qq_45906219
# pip install pymysql

# 1. 导入这个包
import pymysql

# 2. 创建数据库
# 3. 连接数据库  pymysql,  mysqldb
db = pymysql.connect(host='127.0.0.1', user="root", db="tornado",
                     passwd="whnxtz9.9", port=3306)

# 4. 获取游标地址
cursor = db.cursor()


# 5. 进行数据的提交  id, name, age, now_time
# try:
#     cursor.execute("insert into test_sql values(0, 'Tony', '16', now());")
#     db.commit()
#     print("insert into test_sql values(0, 'Tony', '16', now());")
# except Exception as e:
#     db.rollback()
#     cursor.close()


def save_to_sql(content):
    # *arg 接受列表， 元组的值
    #  **items  自动接受字典的值

    try:
        cursor.execute(
            f"insert into test_sql values(0, '{content['name']}', '{content['age']}', now());")
        db.commit()
    except Exception as e:
        db.rollback()


if __name__ == '__main__':
    # 6. 从字典，或者其他生成器中拿到数据，进行数据库的提交
    items = [
        {"name": "bob", "age": "15"},
        {"name": "mary", "age": "17"},
        {"name": "sir", "age": "18"},
    ]
    for i in items:
        save_to_sql(i)

    # 关闭数据库
    cursor.close()
    db.close()
