import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Line, Station
import pandas as pd
from datetime import datetime

SQLALCHEMY_DATABASE_URI = 'sqlite:///mrt.db'
DATA_FILE_NAME = 'StationMap.csv'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def Load_Data(file_name):
    data = pd.read_csv(file_name)
    return data.values.tolist()

try:
    row_list = Load_Data(DATA_FILE_NAME)
    line_set = set()

    # Populate lines
    for row in row_list:
        line_set.add(row[0][0:2])

    for line_name in line_set:
        line = Line(
            name=line_name
        )
        session.add(line)

    session.commit()

    lines = session.query(Line).order_by(Line.id.asc())
    line_dict = {line.name:line.id for line in lines}

    # Populate stations
    for row in row_list:
        station = Station(
            name = str(row[1]),
            line_id = line_dict[str(row[0][0:2])],
            code_number = int(row[0][2:]),
            opening_date = datetime.strptime(row[2], '%d %B %Y').date(),
        )
        session.add(station)
    
    session.commit()
except:
    print("Unexpected error:", sys.exc_info()[0])
    # Rollback the changes on error
    session.rollback()
finally:
    # Close the connection
    session.close()