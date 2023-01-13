# This script generates compatibility reports for newly added plants in the database.
# It does this in the following order:
# • Go through each pair of plants starting at the last analyzed pair
# • Run algorithm modules on them by a database check
# • Write the report back to the database
import logging
import algorithm
import utils
from schema import (
    init_db,
    reports_table,
    plants_table
)

# Selects plant species from a given start point
def get_plants_from(con, start = None):
    stmt = plants_table.select()
    if start:
        stmt = stmt.where(plants_table.c.id > start)
    return con.execute(stmt)

# The main loop for companionship reporting
def main():
    db = init_db()
    logging.basicConfig(level=logging.NOTSET)
    with db.connect() as con:
        for plant1 in get_plants_from(con):
            for plant2 in get_plants_from(con, plant1.id):
                logging.info(f'Analyzing {plant1.name} x {plant2.name}...')
                utils.new_report()
                for rule in utils.get_rules():
                    rule(plant1, plant2)
                stmt = reports_table.insert().values(
                    plant1 = plant1.id,
                    plant2 = plant2.id,
                    report = utils.get_report()
                )
                con.execute(stmt)

# Run as a script
if __name__ == '__main__':
    main()