import os
import random
import re
import uuid

from flask import Blueprint, render_template, jsonify, session, request

from flask_login import logout_user,login_required,login_user,LoginManager

from utils.functions import is_login

login_manage = LoginManager()


from app.models import User, House, Order

user_blue = Blueprint('user',__name__)

@user_blue.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/',methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile,imagecode,passwd,passwd2]):
       return jsonify({'code':1001,'msg':'请填写完整的参数'})
    # 2.验证手机号正确
    if not re.match('^1[3456789]\d{9}$',mobile):
        return jsonify({'code':1002,'msg':'手机号不正确'})
    # 3.验证图片验证码
    if session['image_code'] != imagecode:
        return jsonify({'code':1003,'msg':'验证码不正确'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code':1004,'msg':'密码不一致'})
    #  验证手机号受否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code':1005,'msg':'手机号已经被注册，请重新注册'})
    #　创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/code/',methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址(不推荐)
    # 方式2：后端只生成随机参数，返回给页面，在页面中在生成图片(前端做)
    s = '1234567890qwertyuiopasdfghjklQWERTYUIOPASDFGHJKL'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['image_code'] = code
    return jsonify({'code':200,'msg':'请求成功','data':code})


@user_blue.route('/login/',methods=['GET'])
def login():
    return render_template('login.html')

@user_blue.route('/login/',methods=['POST'])
def my_login():
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    if not all([mobile,passwd]):
        return jsonify({'code':1001,'msg':'请填写完整的参数'})
    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code':1002,'msg':'用户不存在,请先注册'})
    if not user.check_pwd(passwd):
        return jsonify({'code':1003,'msg':'密码不正确'})
    # 向session中存键值对
    login_user(user)
    return jsonify({'code':200,'msg':'登陆成功'})


@user_blue.route('/my/',methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user_blue.route('/my_message/',methods=['GET'])
@login_required
def my_message():
    # 获取用户基本信息
    id = session.get('user_id')
    user = User.query.filter_by(id=id).first()
    return jsonify({'code':200,'msg':'请求成功','data':user.to_basic_dict()})

@login_manage.user_loader
def load_user(user_id):
    # 定义被login_manage装饰的回调函数
    # 返回的是当前登陆的用户对象
    return User.query.filter(User.id==user_id).first()


@user_blue.route('/logout/',methods=['GET'])
def logout():
    del session['user_id']
    return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/profile/',methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user_blue.route('/avatar/',methods=['PATCH'])
def my_profile():
    # 获取图片
        avatar = request.files.get('avatar')
        # 拼接图片保存路径路径(拼接绝对路径，D:\wordspace\8.flask\ihome\static\media)
        # 1.找到D:\wordspace\8.flask\ihome
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 2.将static拼接上去，D:\wordspace\8.flask\ihome\static
        STATIC_DIR = os.path.join(BASE_DIR,'static')
        # 3. 将media拼接上去，D:\wordspace\8.flask\ihome\static\media
        MEDIA_DIR = os.path.join(STATIC_DIR,'media')
        # 生成图片名字
        filename = str(uuid.uuid4())
        # 将原图片的格式结尾切割下来
        a = avatar.mimetype.split('/')[-1:][0]
        # 拼接图片名称
        name = filename+'.' + a
        # 4. 拼接图片最终保存路径
        path = os.path.join(MEDIA_DIR,name)
        # 保存图片
        avatar.save(path)
        id = session.get('user_id')
        user = User.query.get(id)
        user.avatar = name
        user.add_update()
        return jsonify({'code':200,'msg':'请求成功','data':name})


@user_blue.route('/name/',methods=['PATCH'])
def name():
    name = request.form.get('name')
    id = session.get('user_id')
    user = User.query.get(id)
    user.name = name
    user.add_update()
    return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/auth/',methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blue.route('/my_auth/',methods=['PATCH','GET'])
def my_auth():
    if request.method == 'GET':
        id = session.get('user_id')
        user = User.query.get(id)
        if all([user.id_name,user.id_card]):
            return jsonify({'code':200,'msg':'请求成功','data':user.to_auth_dict()})
        return jsonify({'code':1001,'msg':'请求成功'})
    if request.method == 'PATCH':
        id_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        if all([id_name,id_card]):
            id = session.get('user_id')
            user = User.query.get(id)
            if re.match('\d{6}(19|20)\d{2}[01]\d[0123]\d{4}[\dxX]',id_card ):
                user.id_name = id_name
                user.id_card = id_card
                user.add_update()
                return jsonify({'code':200,'msg':'请求成功','data':user.to_auth_dict()})
            else:
                return jsonify({'code':1002,'msg':'身份证格式错误'})
        else:
            return jsonify({'code':1003,'msg':'信息填写不完整，请补全信息'})


@user_blue.route('/index/',methods=['GET'])
def index():
    return render_template('index.html')


@user_blue.route('/my_index/',methods=['GET'])
def my_index():
    house_info = []
    houses = House.query.all()
    for house in houses:
        house_info.append(house.to_dict())
    return jsonify({'code':200,'msg':'请求成功','data':house_info})

@user_blue.route('/search/',methods=['GET'])
def search():
    return render_template('search.html')


@user_blue.route('/my_search/',methods=['GET'])
def my_search():
    order_id = []
    aid = int(request.args.get('aid'))
    aname = request.args.get('aname')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    houses = House.query.filter_by(area_id=aid).all()
    for house in houses:
        order = Order.query.filter_by(house_id=house.id).first()
        if order.status != 'REJECTED':
            one = Order.query.filter(Order.begin_date<sd,Order.end_date>sd,Order.end_date<ed ).all()
            two = Order.query.filter(Order.begin_date>sd,Order.begin_date<ed,Order.end_date>ed).all()
            three = Order.query.filter(Order.begin_date>sd,Order.begin_date<ed,Order.end_date>sd,Order.end_date<ed).all()
            four = Order.query.filter(Order.begin_date<sd,Order.end_date>ed).all()
            if one:
                for i in one:
                    order_id.append(i.house_id)



    return jsonify({'code':200,'msg':200})


