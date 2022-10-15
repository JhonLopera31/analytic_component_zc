from pydantic import BaseModel

class Location (BaseModel):
    lng:float
    lat:float