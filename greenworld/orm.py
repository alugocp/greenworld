"""
This module defines the SQLAlchemy ORM database schema
"""
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
    JSON,
)

# Metadata object for SQLAlchemy
meta = MetaData()

# Database connection object
DB = None


# This function initializes or retrieves a singular database connection object
def init_db():
    """
    Initializes the database object to be used throughout this process
    """
    # pylint: disable-next=global-statement
    global DB
    if not DB:
        dbstring = os.getenv("GREENWORLD_DB")
        if not dbstring:
            raise ValueError(
                "Please set GREENWORLD_DB environment variable to an ODBC string"
            )
        DB = create_engine(dbstring)
    return DB


# Tracks past report progress for data entry optimization
memory_table = Table("memory", meta, Column("last_analyzed", Integer, nullable=False))

# Tracks reports of plant compatibility
reports_table = Table(
    "reports",
    meta,
    Column("plant1", Integer, ForeignKey("plants.id"), nullable=False),
    Column("plant2", Integer, ForeignKey("plants.id"), nullable=False),
    Column("score", Numeric),
    Column("report", JSON, nullable=False),
)

# Tracks plant data
plants_table = Table(
    "plants",
    meta,
    # General
    Column("id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("species", String, nullable=False),
    Column("family", String, nullable=False),
    # Morphology
    Column("growth_habit", Integer),  # GrowthHabit enum
    # Nutrients
    Column("nitrogen", Integer),  # Nitrogen enum
    # Preferred environment
    Column("sun", Integer),  # Sun enum
    Column("soil", Integer),  # Soil enum
    Column("pH", NumericRangeType),  # Floating point pH scale
    Column("drainage", Integer),  # Drainage enum
    # Citations
    Column("citations", JSON, nullable=False),
)

# Tracks works cited for any data points
works_cited_table = Table(
    "works_cited",
    meta,
    Column("id", Integer, Identity(), primary_key=True),
    Column("citation", String, nullable=False),
)

# Tracks non-plant species
other_species_table = Table(
    "other_species",
    meta,
    Column("id", Integer, Identity(), primary_key=True),
    Column("species", String, nullable=False),
    Column("name", String, nullable=False),
    Column("family", String),
)

# Tracks relationships between plant and non-plant species
ecology_other_table = Table(
    "ecology_other",
    meta,
    Column("plant", Integer, ForeignKey("plants.id"), nullable=False),
    Column("non_plant", Integer, ForeignKey("other_species.id"), nullable=False),
    Column("relationship", Integer, nullable=False),  # Ecology enum
    Column("citation", Integer, ForeignKey("works_cited.id"), nullable=False),
)

# Tracks relationships between plant and other plant species
ecology_plant_table = Table(
    "ecology_plant",
    meta,
    Column("plant", Integer, ForeignKey("plants.id"), nullable=False),
    Column("target", Integer, ForeignKey("plants.id"), nullable=False),
    Column("relationship", Integer, nullable=False),  # Ecology enum
    Column("citation", Integer, ForeignKey("works_cited.id"), nullable=False),
)
