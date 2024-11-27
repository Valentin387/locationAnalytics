
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .Vehiculo import Vehiculo

# Define ObjectId as a valid type for Pydantic to handle
class ObjectIdField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class VehiculoPlusLocation(BaseModel):
    id: ObjectIdField = Field(..., alias="_id")
    vehiculo: Vehiculo
    latitud: float
    longitud: float
    timeStamp: datetime
    timeStampServer: datetime
    speed: float
    batteryPercentage: Optional[float] = None  # Make this field optional
    usuario: ObjectIdField
    applicationVersion: Optional[str] = None  # Optional field
    locationAccuracy: Optional[float] = None  # Optional field




# {
#     '_id': ObjectId('6743fddc0769425760034260'),
#     'vehiculo': {
#         '_id': '0', 
#         'color': {'code': 'X', 'color': 'X'}, 
#         'foto': 'X', 'marca': 'X', 'modelo': 0, 
#         'placa': 'TRIQUE-DOSYMEDIO', 
#         'serie': 'X', 
#         'status': 'X', 
#         'tipo': 'X'
#         },
#     'latitud': '5.9341395', 
#     'longitud': '-74.5693753', 
#     'timeStamp': datetime.datetime(2024, 11, 25, 4, 32, 27, 47000), 
#     'timeStampServer': datetime.datetime(2024, 11, 25, 4, 32, 28, 76000), 
#     'speed': '0.30000782', 
#     'batteryPercentage': '100', 
#     'usuario': ObjectId('6741137d0769425760ffd868'), 
#     '__v': 0
# }