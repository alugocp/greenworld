# This script generates compatibility reports for newly added plants in the database.
# It does this in the following order:
# • Go through each pair of plants starting at the last analyzed pair
# • Run algorithm modules on them by a database check
# • Write the report back to the database
from schema import (
    init_db,
    reports,
    plants
)

# Selects plant species from a given start point
def get_plants_from(con, start = None):
    stmt = plants.select()
    if start:
        stmt = stmt.where(plants.c.id > start)
    return con.execute(stmt)

# Calculates a single companionship report
def generate_report(plant1, plant2):
    return {}

# The main loop for companionship reporting
def main():
    db = init_db()
    with db.connect() as con:
        for plant1 in get_plants_from(con):
            for plant2 in get_plants_from(con, plant1.id):
                analysis = generate_report(plant1, plant2)
                stmt = reports.insert().values(
                    plant1 = plant1.id,
                    plant2 = plant2.id,
                    report = analysis
                )
                con.execute(stmt)

# Run as a script
if __name__ == '__main__':
    main()