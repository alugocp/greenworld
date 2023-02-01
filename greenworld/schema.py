import os
from sqlalchemy_utils import NumericRangeType
from sqlalchemy import (
    create_engine,
    ForeignKey,
    MetaData,
    Identity,
    Table,
    Column,
    Integer,
    String,
    JSON
)

# Metadata object for SQLAlchemy
meta = MetaData()

# Database connection object
DB = None

# This function initializes or retrieves a singular database connection object
def init_db():
    # pylint: disable=global-statement
    global DB
    # pylint: enable=global-statement
    if not DB:
        dbstring = os.getenv('GREENWORLD_DB')
        if not dbstring:
            raise Exception('Please set GREENWORLD_DB environment variable to an ODBC string')
        DB = create_engine(dbstring)
    return DB

memory_table = Table('memory', meta,
    Column('last_analyzed', Integer)
)

reports_table = Table('reports', meta,
    Column('plant1', Integer, ForeignKey('plants.id')),
    Column('plant2', Integer, ForeignKey('plants.id')),
    Column('report', JSON)
)

# TODO revisit sources for seed data and convert to these official units
plants_table = Table('plants', meta,
    # General
    Column('id', Integer, Identity(), primary_key = True),
    Column('name', String),
    Column('species', String),

    # Morphology
    Column('growth_habit', Integer),
    Column('fruit_weight', NumericRangeType), # Grams
    Column('height', NumericRangeType), # Meters
    Column('spread', NumericRangeType), # From one extermity to the other (Meters)
    Column('length', NumericRangeType), # Meters
    Column('root_spread', NumericRangeType), # From one extremity to the other (Meters)
    Column('root_depth', NumericRangeType), # Meters

    # Nutrients
    Column('nitrogen', Integer),

    # Preferred environment
    Column('temperature', NumericRangeType), # Celsius
    Column('sun', Integer),
    Column('soil', Integer),
    Column('pH', NumericRangeType),
    Column('drainage', Integer)
)
