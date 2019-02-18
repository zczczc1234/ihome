import os
import uuid

from flask import render_template,session,Blueprint,jsonify,request

from app.models import User, Area, Facility, House, HouseImage
from utils.functions import is_login

house_blue = Blueprint('house',__name__)

@house_blue.route('/myhouse/',methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')

@house_blue.route('/my_myhouse/',methods=['GET'])
def my_myhouse():
    if request.method == 'GET':
        house = []
        id = session.get('user_id')
        user = User.query.get(id)
        if all([user.id_name,user.id_card]):
            houses = House.query.filter_by(user_id=id).all()
            for h in houses:
                house.append(h.to_dict())
            return jsonify({'code':200,'msg':'请求成功','data':house})
        else:
            return jsonify({'code':1001,'msg':'请先完成实名认证'})


@house_blue.route('/newhouse/',methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@house_blue.route('/area/',methods=['GET'])
def area():
    area = []
    areas = Area.query.all()
    for i in areas:
        area.append(i.to_dict())
    return jsonify({'code':200,'msg':'请求成功','data':area})


@house_blue.route('/house_facility/',methods=['GET'])
def house_facility():
    facility = []
    facilities = Facility.query.all()
    for i in facilities:
        facility.append(i.to_dict())
    return jsonify({'code':200,'msg':'请求成功','data':facility})


@house_blue.route('/house_info/',methods=['POST'])
def house_info():
    title = request.form.get('title')
    price = request.form.get('price')
    area_id = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    facility = request.form.getlist('facility')
    house = House()
    house.user_id = session.get('user_id')
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    f = []
    for i in facility:
        fac = Facility.query.filter_by(id=i).first()
        f.append(fac)
    house.facilities = f
    house.add_update()
    return jsonify({'code':200,'msg':'请求成功','data':house.id})


@house_blue.route('/house_image/',methods=['POST'])
def house_image():
    house_id = request.form.get('house_id')
    print(house_id)
    house_image = request.files.get('house_image')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(BASE_DIR,'static')
    MEDIA_DIR = os.path.join(STATIC_DIR,'media')
    filename = str(uuid.uuid4())
    image = house_image.mimetype.split('/')[-1:][0]
    name = filename+'.'+image
    path = os.path.join(MEDIA_DIR,name)
    house_image.save(path)
    house = House.query.filter_by(id=house_id).first()
    if not house.index_image_url:
        house.index_image_url = name
        house.add_update()
    houseimage = HouseImage()
    houseimage.house_id = house_id
    houseimage.url = name
    houseimage.add_update()
    return jsonify({'code':200,'msg':'请求成功','data':name})


@house_blue.route('/detail/',methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blue.route('/detail/<int:id>/',methods=['GET'])
def my_datail(id):
    house = House.query.filter_by(id=id).first()
    house_info = [house.to_full_dict()]
    return jsonify({'code':200,'msg':'请求成功','data':house_info})

