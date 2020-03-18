import sys
import unittest
import json
import logging
from config import Config, TestingConfig
from app import app, db
from app.models import Station, Sensor

# Test cases for /stations
class StationModelCase(unittest.TestCase):
    # Set up the database and a text logger
    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.StreamHandler(sys.stdout))
        db.create_all()
        
    def test_response(self):
        response= self.app.test_client().get('/stations')
        self.assertEqual(response.status_code, 200)
        
    # Test sqlite insertion and get, /stations [GET]
    def test_get(self):
        # Create and insert two stations and two sensors into sqlite
        se1= Sensor(reads='Humidity')
        se2= Sensor(reads='Temprature')
        st1= Station(name='Jx05t', active=True, sensors=[se1,se2])
        st2= Station(name='Zy99p', active=True)
        db.session.add_all([st1,st2])
        db.session.commit()
        a1= db.session.query(Station).filter_by(name=st1.name).one()
        a2= db.session.query(Station).filter_by(name=st2.name).one()
        
        # Check if they are inserted
        self.assertEqual(a1,st1)
        self.assertEqual(a2,st2)

        # Check the relationship Stations -< Sensor
        self.assertEqual(a1.sensors.all(),[se1,se2])
        self.assertEqual(a2.sensors.all(),[])
        
        # Send an API request to get stations
        response= self.app.test_client().get('/stations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        
        # Check if they exist in the response
        item_ids_returned = [item["id"] for item in data['data']]
        self.assertIn(a1.id,item_ids_returned)
        self.assertIn(a2.id,item_ids_returned)
        for item in data['data']:
            if(item["id"]==a1.id):
                self.assertEqual(item["name"],a1.name)

    # Create a station through the API, /stations [POST]
    def test_create(self):
        station= {
            "name": "HGp78",
            "active": False
        }
        station_payload = json.dumps(station)
        response= self.app.test_client().post('/stations', headers={"Content-Type":"application/json"}, data= station_payload)
        
        # Check the response
        self.assertEqual(response.status_code, 201)
        
        # Retrieve the item through sqlite
        a1= db.session.query(Station).filter_by(id=response.json["id"]).one()        
        # Check if it is the same
        self.assertEqual(a1.name,station["name"])
    
    # Test the update, /stations/<int:id> [PUT]
    def test_update(self):
        # Create and insert an item into sqlite
        st2= Station(name='Zy99p', active=True)
        db.session.add_all([st2])
        db.session.commit()
        
        # Payload to update the item
        station= {
            "name": "HGp78",
            "active": False
        }
        station_payload = json.dumps(station)
        a2= db.session.query(Station).filter_by(name=st2.name).one()
        
        # Request to update the item through the API
        response= self.app.test_client().put('/stations/'+str(a2.id), headers={"content-type":"application/json"}, data= station_payload)
        
        # Retrieve the item through sqlite
        a2= db.session.query(Station).filter_by(id=a2.id).one()
        # Check if correctly updated
        self.assertEqual(a2.name,station["name"])
 
    # Test the delete request, /stations/<int:id> [DELETE]
    def test_delete(self):
        # Create and insert stations and sensors into sqlite
        se1= Sensor(reads='Humidity')
        se2= Sensor(reads='Temprature')
        st1= Station(name='Jx05t', active=True, sensors=[se1,se2])
        st2= Station(name='Zy99p', active=True)
        db.session.add_all([st1,st2])
        db.session.commit()
        a1= db.session.query(Station).filter_by(name=st1.name).one()
        a2= db.session.query(Station).filter_by(name=st2.name).one()
        
        # Check if correctly inserted
        self.assertEqual(a1.name,st1.name)
        self.assertEqual(a2.name,st2.name)
        self.assertEqual(a1.sensors.count(),2)
        
        # Request delete through the API
        response= self.app.test_client().delete('/stations/'+str(a1.id))        
        
        # Retrieve items through sqlite
        a1= db.session.query(Station).filter_by(name=st1.name).scalar()
        a2= db.session.query(Station).filter_by(name=st2.name).scalar()
        ses= db.session.query(Sensor).count()
        
        # Check if correctly deleted
        self.assertEqual(a1,None)
        self.assertNotEqual(a2,None)
        
        # Check if deleting cascaddes to sensors correctly
        self.assertEqual(ses,0)        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main(verbosity=2)