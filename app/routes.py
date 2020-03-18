from app import app


from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Station, Sensor
from app.errorhandling import request_failed


@app.route('/')
@app.route('/index')
def readme():
    docs= """
    Usage:
    
    Station -< Sensor;
    
    GET     /stations
    ;GET     /stations/<int:id>
    ;GET     /stations/<int:id>/sensors
    ;POST    /stations
    ;PUT     /stations/<int:id>
    ;DELETE  /stations/<int:id>
    """
    return docs


@app.route('/stations/<int:id>', methods=['GET'])
def get_station(id):
    return jsonify(Station.query.get_or_404(id).packin())


@app.route('/stations', methods=['GET'])
def get_stations():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Station.collect(Station.query, page, per_page, 'get_stations')
    return jsonify(data)


@app.route('/stations/<int:id>/sensors', methods=['GET'])
def get_sensors(id):
    station = Stations.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Station.collect(station.sensors, page, per_page,
                                   'get_sensors', id=id)
    return jsonify(data)


@app.route('/stations', methods=['POST'])
def create_station():
    data = request.get_json() or {}
    if 'name' not in data or 'active' not in data:
        return bad_request('Missing fields -name -active')
    if Station.query.filter_by(name=data['name']).first():
        return bad_request('Station with that name already exists.')
    station = Station()
    station.unpack(data, new_station=True)
    db.session.add(station)
    db.session.commit()
    response = jsonify(station.packin())
    response.status_code = 201
    response.headers['Location'] = url_for('get_station', id=station.id)
    return response

@app.route('/stations/<int:id>', methods=['PUT'])
def update_station(id):
    station = Station.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != station.name and \
            Station.query.filter_by(name=data['name']).first():
        return bad_request('Station with that name already exists.')
    station.unpack(data, new_station=False)
    db.session.commit()
    return jsonify(station.packin())

@app.route('/stations/<int:id>', methods=['DELETE'])
def delete_station(id):
    station = Station.query.get_or_404(id)
    db.session.delete(station)
    db.session.commit()
    return jsonify({'result': True})


