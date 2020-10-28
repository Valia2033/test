from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cellphone = Column(String)
    address = Column(String)
    description = Column(String)
    status = Column(String)

    def __init__(self, name, cellphone, address, description, status):
        self.name = name
        self.cellphone = cellphone
        self.address = address
        self.description = description
        self.status = status

    def ToList(self):
        return {'id': self.id, 'name': self.name, 'cellphone': self.cellphone,
                'address': self.address, 'description': self.description, 'status': self.status}

    def __repr__(self):
        return "{'%s', '%s', '%s', '%s', '%s', '%s'}" % \
               (self.id, self.name, self.cellphone, self.address, self.description, self.status)


class Couriers(Base):
    __tablename__ = 'courier'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    zone = Column(String)
    list = Column(String)

    def __init__(self, name, zone, list):
        self.name = name
        self.zone = zone
        self.list = list

    def __repr__(self):
        return "{'%s', '%s', '%s', '%s'}" % (self.id, self.name, self.zone, self.list)


class Zones(Base):
    __tablename__ = 'zone2'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    cor = Column(String)

    def __init__(self, title, cor):
        self.title = title
        self.cor = cor

    def __repr__(self):
        return "{'%s', '%s', '%s'}" % (self.id, self.title, self.cor)
