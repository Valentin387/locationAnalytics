
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class VehiculoPlusLocation(BaseModel):
    _id: str
    vehiculo: dict
    latitud: float
    longitud: float
    timeStamp: datetime
    timeStampServer: datetime
    speed: float
    batteryPercentage: Optional[float] = None  # Make this field optional
    usuario: str
    applicationVersion: Optional[str] = None  # Optional field
    locationAccuracy: Optional[float] = None  # Optional field

    class Config:
        # Allow MongoDB ObjectId to be serialized as a string
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str,  # Convert ObjectId to string

        }



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