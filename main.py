from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request, abort
from classes import Zones, Couriers, Orders, Base
import search_zone

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# swagger specific
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL,)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# end swagger specific

engine = create_engine('sqlite:///foo.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
session.commit()


# Поиск курьера для выполнения заказа
@app.route("/api/admin/search", methods=['PUT'])
def search_order():
    a = []
    for row in session.query(Zones).all():
        try:
            t = search_zone.zone(row.cor, request.json['Cor'])
        except:
            t = False
        if t:
            for cour in session.query(Couriers).filter_by(zone=row.title):
                a += [{'id': cour.id, 'name': cour.name,'zone': cour.zone, 'OrderList': cour.list}]
    session.commit()
    if a:
        return jsonify(a), 201
    else:
        return jsonify({'Доступный курьер не найден': 404})


# Добавить курьеру заказ
@app.route("/api/admin/assign", methods=['PUT'])
def assing_order():
    if not request.json:
        abort(400)
    a = {}
    for row in session.query(Couriers).filter_by(id=request.json['CourierID']):
        row.list += ' '
        row.list += str(request.json['OrderID'])
        a = {'id': row.id, 'name': row.name, 'zone': row.zone, 'OrderList': row.list}

    session.commit()
    return jsonify(a), 201


# Обновление заказов курьером или администратором
@app.route('/api/<string:cser>', methods=['PUT'])
def update_task(cser):
    if not request.json:
        abort(400)
    a = {}
    if cser == 'admin' or cser == 'courier':
        for row in session.query(Orders).filter_by(id=request.json['id']):
            row.status = request.json['status']
            a = Orders.ToList(row)
    session.commit()
    return jsonify(a), 201


# Получение списка(конкретного заказа)
@app.route("/api/admin/<int:order_id>", methods=['GET'])
def get_order(order_id=0):
    a = []
    if order_id != 0:
        for row in session.query(Orders).filter_by(id=order_id):
            a = [Orders.ToList(row)]
    elif order_id == 0:
        for row in session.query(Orders).all():
            a += [Orders.ToList(row)]
    session.commit()

    return jsonify(a), 201


# получение заказов курьером
@app.route("/api/courier/<int:courier_id>", methods=['GET'])
def get_orders(courier_id):
    a = []
    for row in session.query(Couriers).filter_by(id=courier_id):
        for i in row.list.split():
            for order in session.query(Orders).filter_by(id=i):
                a += [Orders.ToList(order)]
    session.commit()

    return jsonify(a), 201


# Добавление заказа клиентом
@app.route('/api/client', methods=['POST'])
def create_order():
    if not request.json:
        abort(400)
    order = Orders(request.json['name'], request.json['cellphone'],
                   request.json['address'], request.json['description'], request.json['status'])

    session.add(order)
    session.commit()
    return jsonify({}), 201


# Обновление заказа клиентом
@app.route('/api/client', methods=['PUT'])
def update_order():
    for row in session.query(Orders).filter_by(id=request.json['id']):
        if 'name' in request.json:
            row.name = request.json['name']
        if 'cellphone' in request.json:
            row.cellphone = request.json['cellphone']
        if 'address' in request.json:
            row.address = request.json['address']
        if 'description' in request.json:
            row.description = request.json['description']
        if 'status' in request.json:
            row.status = request.json['status']
    session.commit()
    return request.json, 200


# запросы владельца
@app.route('/api/owner/zone', methods=['POST'])
def add_zone():
    if not request.json:
        abort(400)
    zone = Zones(request.json['title'], request.json['cor'])
    session.add(zone)

    session.commit()
    return '201'


@app.route('/api/owner/courier', methods=['POST'])
def add_courier():
    if not request.json:
        abort(400)
    cour = Couriers(request.json['name'], '', '')
    session.add(cour)
    session.commit()
    return '201'


# задание зоны для курьера
@app.route('/api/owner/setzone', methods=['PUT'])
def set_zone():
    if not request.json:
        abort(400)
    for row in session.query(Couriers).filter_by(id=request.json['courier_id']):
        row.zone = request.json['zone']
    session.commit()
    return [], 201


# Получить список зон доставки и курьеров
@app.route("/api/owner/get/<string:cdir>", methods=['GET'])
def get(cdir):
    a = []
    if cdir == 'couriers':
        for row in session.query(Couriers).all():
            print(row)
            a += [{"id": row.id, "name": row.name, "zone": row.zone, "list": row.list}]

    elif cdir == 'zones':
        for row in session.query(Zones).all():
            a += [{"id": row.id, "title": row.title, "cor": row.cor}]
    session.commit()
    return jsonify(a), 201


# удаление записи из базы данных
@app.route('/api/owner/delete/<string:cdir>/<int:_id>', methods=['DELETE'])
def delete(cdir, _id):
    if cdir == 'orders':
        print(cdir, _id)
        for row in session.query(Orders).filter_by(id=_id):
            session.delete(row)
    elif cdir == 'zones':
        for row in session.query(Zones).filter_by(id=_id):
            session.delete(row)
    elif cdir == 'couriers':
        for row in session.query(Couriers).filter_by(id=_id):
            session.delete(row)
    else:
        return '404'
    session.commit()
    return '200'


if __name__ == '__main__':
    app.run(debug=True)
