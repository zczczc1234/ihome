

from flask import Blueprint, render_template, jsonify, request, session

from app.models import House, Order

order_blue = Blueprint('order',__name__)

@order_blue.route('/booking/',methods=['GET'])
def booking():
    return render_template('booking.html')


@order_blue.route('/my_booking/<int:id>/',methods=['GET'])
def my_booking(id):
    house = House.query.filter_by(id=id).first()

    return jsonify({'code':200,'msg':'请求成功','data':house.to_dict()})


@order_blue.route('/submit_order/<int:id>/',methods=['POST'])
def submit_order(id):
    order = Order()
    order.user_id = session.get('user_id')
    order.house_id = id
    order.begin_date = request.form.get('startDate')
    order.end_date = request.form.get('endDate')
    order.days = request.form.get('days')
    order.house_price = request.form.get('price')
    order.amount = request.form.get('amount')
    order.add_update()
    return jsonify({'code':200,'msg':'请求成功'})


@order_blue.route('/order/',methods=['GET'])
def order():
    return render_template('orders.html')


@order_blue.route('/my_order/',methods=['GET'])
def my_order():
    order = []
    status = {
        "WAIT_ACCEPT":'待接单',
        "WAIT_PAYMENT":'待支付',
        "PAID":'已支付',
        "WAIT_COMMENT":'待评价',
        "COMPLETE":'已完成',
        "CANCELED":'已取消',
        "REJECTED" :'已拒单'
    }
    orders = Order.query.filter_by(user_id=session.get('user_id')).all()
    for i in orders:
        order.append(i.to_dict())
    return jsonify({'code':200,'msg':'请求成功','data':order,'status':status})


@order_blue.route('/lorder/',methods=['GET'])
def lorder():
    return render_template('lorders.html')


@order_blue.route('/my_lorder/',methods=['GET'])
def my_lorder():
    house_id = []
    order = []
    status = {
        "WAIT_ACCEPT": '待接单',
        "WAIT_PAYMENT": '待支付',
        "PAID": '已支付',
        "WAIT_COMMENT": '待评价',
        "COMPLETE": '已完成',
        "CANCELED": '已取消',
        "REJECTED": '已拒单'
    }
    house = House.query.filter_by(user_id=session.get('user_id')).all()
    for i in house:
        house_id .append(i.id)
    for id in house_id:
        orders = Order.query.filter_by(house_id=id).first()
        order.append(orders.to_dict())
    return jsonify({'code':200,'msg':'请求成功','data':order,'status':status})


@order_blue.route('/accept_order/',methods=['PATCH'])
def accept_order():
    orderId = request.form.get('orderId')
    status = request.form.get('status')
    comment = request.form.get('comment')
    order = Order.query.filter_by(id=orderId).first()
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify({'code':200,'msg':'请求成功'})