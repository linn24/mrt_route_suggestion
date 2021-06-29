import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
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


class Traffic(Base):
    """
    Traffic information for each MRT line and line change at specific period
    """
    __tablename__ = 't_traffic'

    id = Column(Integer, primary_key=True)
    # when line_id is not specified, the record is meant for train line change
    line_id = Column(Integer, ForeignKey('t_line.id'))
    start_hour = Column(Integer)
    end_hour = Column(Integer)
    is_weekend = Column(Boolean, default=False)
    is_operating = Column(Boolean, default=True)
    delay_in_minutes = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'line_id': self.line_id,
            'start_hour': self.start_hour,
            'end_hour': self.end_hour,
            'is_weekend': self.is_weekend,
            'is_operating': self.is_operating,
            'delay_in_minutes': self.delay_in_minutes,
        }


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)