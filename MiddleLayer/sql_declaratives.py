import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    latitude = Column(DECIMAL(6))
    longitude = Column(DECIMAL(6))


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    locationid = Column(Integer, ForeignKey('locations.id'))
    status = Column(String(20))
    temp = Column(Float)
    decible = Column(Float)


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, nullable=False)
    locationID = Column(Integer, ForeignKey('locations.id'))
    deviceID = Column(Integer, ForeignKey('devices.id'))
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    type = Column(String(20), nullable=False)
    value = Column(DECIMAL(5), nullable=False)
    units = Column(String(10))

    Location = relationship(Location)
    Device = relationship(Device)