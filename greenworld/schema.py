import os
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
db = None

# This function initializes or retrieves a singular database connection object
def init_db():
    global db
    if not db:
        dbstring = os.getenv('GREENWORLD_DB')
        if not dbstring:
            raise Exception('Please set GREENWORLD_DB environment variable to an ODBC string')
        db = create_engine(dbstring)
    return db

plants = Table('plants', meta,
    Column('id', Integer, Identity(), primary_key = True),
    Column('name', String)
)

reports = Table('reports', meta,
    Column('plant1', Integer, ForeignKey('plants.id')),
    Column('plant2', Integer, ForeignKey('plants.id')),
    Column('report', JSON)
)