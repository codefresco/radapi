from app import db
from flask import url_for
from paginationhelper import PaginationMixin

class Station(PaginationMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    active = db.Column(db.Boolean())
    sensors = db.relationship('Sensor', cascade='all, delete', backref = 'ofstation', lazy = 'dynamic')
    def __repr__(self):
        return '<Station {}>'.format(self.name)
    def packin(self):
        data = {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            '_links': {
                'self': url_for('get_station', id=self.id),
                'sensors': url_for('get_sensors', id=self.id),
            }
        }
        return data

    def unpack(self, data, new_station=False):
        for field in ['name', 'active']:
            if field in data:
                setattr(self, field, data[field])

class Sensor(PaginationMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reads = db.Column(db.String(64))
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    def __repr__(self):
        return '<Sensor {}>'.format(self.reads)

