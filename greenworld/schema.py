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
    Numeric,
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

# Tracks past report progress for data entry optimization
memory_table = Table('memory', meta,
    Column('last_analyzed', Integer)
)

# Tracks reports of plant compatibility
reports_table = Table('reports', meta,
    Column('plant1', Integer, ForeignKey('plants.id')),
    Column('plant2', Integer, ForeignKey('plants.id')),
    Column('range_union_min', Numeric), # The close end of the union of ranges associated with this report
    Column('range_union_max', Numeric), # The far end of the union of ranges associated with this report
    Column('report', JSON)
)

# Tracks plant data
plants_table = Table('plants', meta,
    # General
    Column('id', Integer, Identity(), primary_key = True),
    Column('name', String),
    Column('species', String),

    # Morphology
    Column('growth_habit', Integer), # GrowthHabit enum
    Column('fruit_weight', NumericRangeType), # Grams
    Column('height', NumericRangeType), # Meters
    Column('spread', NumericRangeType), # From one extermity to the other (Meters)
    Column('length', NumericRangeType), # Meters
    Column('root_spread', NumericRangeType), # From one extremity to the other (Meters)
    Column('root_depth', NumericRangeType), # Meters

    # Nutrients
    Column('nitrogen', Integer), # Nitrogen enum

    # Preferred environment
    Column('temperature', NumericRangeType), # Celsius
    Column('sun', Integer), # Sun enum
    Column('soil', Integer), # Soil enum
    Column('pH', NumericRangeType), # Floating point pH scale
    Column('drainage', Integer), # Drainage enum

    # Citations
    Column('citations', JSON)
)

# Tracks works cited for any data points
works_cited_table = Table('works_cited', meta,
    Column('id', Integer, Identity(), primary_key = True),
    Column('citation', String)
)

# Tracks non-plant species
other_species_table = Table('other_species', meta,
    Column('id', Integer, Identity(), primary_key = True),
    Column('species', String)
)

# Tracks relationships between plant and non-plant species
ecology_table = Table('ecology', meta,
    Column('plant', Integer, ForeignKey('plants.id')),
    Column('species', Integer, ForeignKey('other_species.id')),
    Column('relationship', Integer), # Ecology enum
    Column('citation', Integer, ForeignKey('works_cited.id'))
)

# Tracks alelochemicals
allelochemicals_table = Table('allelochemicals', meta,
    Column('id', Integer, Identity(), primary_key = True),
    Column('name', String)
)

# Represents which plants create and/or react to certain allelochemicals
allelopathy_table = Table('allelopathy', meta,
    Column('plant', Integer, ForeignKey('plants.id')),
    Column('allelochemical', Integer, ForeignKey('allelochemicals.id')),
    Column('relationship', Integer), # Allelopathy enum
    Column('citation', Integer, ForeignKey('works_cited.id'))
)
