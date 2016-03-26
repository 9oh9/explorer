from sqlalchemy.types import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geography, Geometry
from sqlalchemy.sql import text
import psycopg2

engine = create_engine('postgresql://uber_app:q94EMtInmu7jBj8sUi3qVQ2yYo8bYWva@localhost:9000/uber')
Base = declarative_base()
Session = sessionmaker(bind=engine)

test_poly = 'POLYGON((-73.994109 40.773058,-73.982479 40.767533,-73.993477 40.752265,-74.004718 40.757145,-73.994109 40.773058))'


def Connect():
    return psycopg2.connect(
        database="uber",
        user="uber_app",
        password="q94EMtInmu7jBj8sUi3qVQ2yYo8bYWva",
        host="localhost",
        port="9000"
    )


class RideService(object):

    def __init__(self, conn):
        self.db = conn.cursor()

    def prepare(self, direction, polygon):
        self.db.execute(
            """SELECT * FROM filter_rides(%s, %s);""",
            (polygon, direction)
        )

    def gen_filter_rides(self):
        for i in range(self.db.rowcount):
            yield self.db.fetchone()

    def filter_rides(self):
        return self.db.fetchall()


class Ride(Base):

    __tablename__ = 'rides'
    id = Column(BigInteger, primary_key=True)
    pickup_time = Column(DateTime(timezone=True))
    dropoff_time = Column(DateTime(timezone=True))
    pickup_latlng = Column(TEXT)
    dropoff_latlng = Column(TEXT)


    @classmethod
    def filter_rides(cls, db, direction, polygon):
        return db.query(cls)\
                .from_statement(text('SELECT * FROM filter_rides(:p, :d);'))\
                .params(p=polygon, d=direction).all()
