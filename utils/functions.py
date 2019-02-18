
# 外层函数嵌套内层函数
# 外层函数返回内层函数
# 内层函数调用外层函数的参数
from flask import session,redirect,url_for

from functools import wraps

def is_login(func):

    @wraps(func)  # 如果不加wraps则会改变被装饰的函数
    def check_status(*args, **kwargs):
        # 判断session 中是否存在登陆的标识user_id
        try:
            session['user_id']
            return func(*args, **kwargs)
        except Exception as e:
            return redirect(url_for('user.login'))
    return check_status