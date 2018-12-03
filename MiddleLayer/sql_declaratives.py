import os
import sys
import datetime
import json

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Float, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    latitude = Column(DECIMAL(6))
    longitude = Column(DECIMAL(6))

    def to_json(self, depth=0):
        j = {}
        j['id'] = self.id
        j['name'] = self.name
        j['latitude'] = str(self.latitude)
        j['longitude'] = str(self.longitude)
        return json.dumps(j)


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    location = Column(Integer, ForeignKey('locations.id'))
    status = Column(String(20))
    temp = Column(Float)
    decibel = Column(Float)

    def to_json(self, depth=0):
        j = {}
        j['id'] = self.id
        j['locationid'] = self.location
        j['status'] = self.status
        j['temp'] = str(self.temp)
        j['decibel'] = str(self.decibel)
        return json.dumps(j)


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, nullable=False)
    locationid = Column(Integer, ForeignKey('locations.id'))
    deviceid = Column(Integer, ForeignKey('devices.id'))
    # timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    type = Column(String(20), nullable=False)
    value = Column(DECIMAL(5), nullable=False)
    units = Column(String(10))

    Location = relationship(Location)
    Device = relationship(Device)

    def to_json(self, depth=1):
        epoch = datetime.datetime.utcfromtimestamp(0)
        j = {}
        j['id'] = self.id
        j['locationid'] = self.locationid
        j['deviceid'] = self.deviceid
        j['timestamp'] = (self.timestamp - epoch).total_seconds() * 1000
        j['type'] = self.type
        j['value'] = str(self.value)
        j['units'] = self.units

        if depth > 0:
            j['location'] = self.Location.to_json(depth-1)
            j['device'] = self.Device.to_json(depth-1)

        return j