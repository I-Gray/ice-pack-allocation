from dataclasses import dataclass
from datetime import datetime


@dataclass
class IceTemperatureRanges:
    temp_min: int
    temp_max: int
    small: int
    medium: int
    large: int


@dataclass
class Box:
    box_id: str
    delivery_date: datetime
    postcode: str
    box_size: str
    cool_pouch_size: str


@dataclass
class BoxAssignedIce:
    box_id: str
    cool_pouch_size: str
    number_of_ices: int
