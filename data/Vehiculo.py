from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

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

class Vehiculo(BaseModel):
    id: ObjectIdField = Field(..., alias="_id")
    color: dict
    foto: str
    marca: str
    modelo: int
    placa: str
    serie: str
    status: str
    tipo: str




#     'vehiculo': {
#         '_id': '0', 
#         'color': {'code': 'X', 'color': 'X'}, 
#         'foto': 'X', 
#         'marca': 'X', 
#         'modelo': 0, 
#         'placa': 'TRIQUE-DOSYMEDIO', 
#         'serie': 'X', 
#         'status': 'X', 
#         'tipo': 'X'
#         },
