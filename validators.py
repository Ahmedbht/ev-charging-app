from pydantic import BaseModel, field_validator
from typing import Optional

class ConnectionTypeValidator(BaseModel):
    id:int
    title :str

class OperatorValidator(BaseModel):
    id :int
    title:str
    website: Optional[str] = None

class StationValidator(BaseModel):
    id :int
    name :str
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_operational: Optional[bool] = None
    number_of_points: Optional[int] = None

    #validate name is not emptyy
    @field_validator("name")
    def name_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    #validate number of points is non-negative
    @field_validator("number_of_points")
    def points_non_negative(cls,value):
        #we check first if its positive
        if value is not None and value <0:
            raise ValueError("Number of points cannot be negative")
        return value