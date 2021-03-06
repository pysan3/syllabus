from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__version__ = "0.1.0"

DATABASE = 'postgres'
USER = 'hueskqfcybpggx'
PASSWORD = '5c7d7524372e83cb57e1d0e264e834cc92c5931cf3ca55ede5736cb462307350'
HOST = 'ec2-54-227-250-19.compute-1.amazonaws.com'
PORT = '5432'
DB_NAME = 'd30uqulffqfitl'

CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

engine = create_engine(CONNECT_STR, echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)

class ClassInfo(Base):
    __tablename__ = 'classinfo'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)
    name = Column('name', String)
    key = Column('key', String)
    term = Column('term', String)
    weekday = Column('weekday', Integer)
    period = Column('period', Integer)
    building = Column('building', Integer)
    room = Column('room', String)

    def __repr__(self):
        return '<ClassInfo(id=%s, year=%s, name=%s, key=%s, term=%s, weekday=%s, period=%s, building=%s, room=%s, )>' \
            % (self.id, self.year, self.name, self.key, self.term, self.weekday, self.period, self.building, self.room)

class FreeRooms(Base):
    __tablename__ = 'freerooms'
    id = Column('id', Integer, primary_key=True)
    day_period = Column('day_period', String)
    term = Column('term', Integer)

    @staticmethod
    def add_column(name, data_type):
        exec(f'FreeRooms.{name} = Column("{name}", data_type)')
        column_name = f'{name}'
        column_type = eval(f'FreeRooms.{name}.type.compile(engine.dialect)')
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (FreeRooms.__tablename__, column_name, column_type))

    @staticmethod
    def add_field(name, data_type):
        exec(f'FreeRooms.{name} = Column("{name}", data_type)', {}, {
            'FreeRooms': FreeRooms,
            'Column': Column,
            'data_type': data_type
        })

class SessionContext(object):
    def __init__(self):
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.flush()
        self.session.commit()
        self.session.close()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)