import uuid
import random

from config import Config
from app import app, db
from app.models import Station, Sensor

class dataGenerator:
    def setUp():
        app.config.from_object(Config)
        db.create_all()
        
        # Possible sensor names
        sensorref = ['Temprature', 'Humidity', 'WindSpeed', 'UV']
        
        # Add 100 stations as example
        for x in range(100):
            # Create random number of random types of sensors
            sensors= [Sensor(reads=sample) for sample in random.sample(sensorref,random.randint(0,4))]
            
            # Random name assigned to station
            st= Station(name=str(uuid.uuid1()), active=True, sensors=sensors)
            db.session.add(st)
        
        db.session.commit()
        
if __name__ == '__main__':
    dataGenerator.setUp()