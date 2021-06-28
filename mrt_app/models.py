import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
SQLALCHEMY_DATABASE_URI = 'sqlite:///mrt.db'


class Line(Base):
    """
    MRT Line information
    """
    __tablename__ = 't_line'
    id = Column(Integer, primary_key=True)
    name = Column(String(2), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }



class Station(Base):
    """
    MRT Station information
    """
    __tablename__ = 't_station'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    line_id = Column(Integer, ForeignKey('t_line.id'))
    code_number = Column(Integer, nullable=False)
    opening_date = Column(Date, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'line_id': self.line_id,
            'code_number': self.code_number,
            'opening_date': self.opening_date,
        }

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)