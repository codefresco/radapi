# A CRUD Prototype with Flask

    API:
    
    GET     /stations
    GET     /stations/<int:id>
    GET     /stations/<int:id>/sensors
    POST    /stations
    PUT     /stations/<int:id>
    DELETE  /stations/<int:id>
    
Run test.py to execute test cases.

Run populateDB.py to populate the database.

## The data model
Data model pictured below represents a set of stations each with multiple sensors

![alt text](https://raw.githubusercontent.com/tarmazdi/radapi/master/docs/dbmodel.PNG)
