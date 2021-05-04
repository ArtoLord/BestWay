from dataclasses import dataclass
from geom import Vector
from typing import Union


@dataclass
class Node:
    __DEGREES_DISTANCE = 111_139

    id: int
    lon: float
    lat: float

    @property
    def vector(self) -> Vector:
        return Vector(self.lon, self.lat)

    def distance_to(self, other):
        return abs(self.vector - other.vector) * self.__DEGREES_DISTANCE

    @classmethod
    def convert_to_degree_distance(cls, meters_distance: float) -> float:
        return meters_distance / cls.__DEGREES_DISTANCE

    @classmethod
    def from_dict(cls, d: Union[(dict, list)]):
        args = {argname: argval.type(d.get(argname)) for argname, argval in cls.__dataclass_fields__.items()}
        return cls(**args)
