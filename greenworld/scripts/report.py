# This script generates compatibility reports for newly added plants in the database.
# It does this in the following order:
# • Go through each pair of plants starting at the last analyzed pair
# • Run algorithm modules on them by a database check
# • Write the report back to the database
import logging
# pylint: disable=unused-import
import greenworld.algorithm
# pylint: enable=unused-import
from greenworld import utils
from greenworld.schema import (
    init_db,
    reports_table,
    memory_table,
    plants_table
)

# Retrieves the last analyzed plant from storage
def get_last_analyzed(con):
    result = con.execute(memory_table.select().limit(1))
    for row in result:
        return row[0]
    return 0

# Updates the last analyzed plant in storage
def set_last_analyzed(con, last):
    con.execute(memory_table.delete())
    con.execute(memory_table.insert().values(last_analyzed = last))

# Selects plant species from a given start point
def get_plants(con, where = None):
    stmt = plants_table.select()
    if where is not None:
        stmt = stmt.where(where)
    return con.execute(stmt)

# The main loop for companionship reporting
def main():
    db = init_db()
    logging.basicConfig(level=logging.NOTSET)
    with db.connect() as con:
        last_plant = None
        last_analyzed = get_last_analyzed(con)
        for plant1 in get_plants(con, plants_table.c.id > last_analyzed).mappings():
            for plant2 in get_plants(con, plants_table.c.id < plant1.id).mappings():
                logging.info('Analyzing %s x %s...', plant2.name, plant1.name)
                utils.new_report()
                for rule in utils.get_rules():
                    rule(plant2, plant1)
                con.execute(reports_table.insert().values(
                    plant1 = plant2.id,
                    plant2 = plant1.id,
                    range_union_min = 0,
                    range_union_max = 0,
                    report = utils.get_report()
                ))
            last_plant = plant1
        if last_plant:
            set_last_analyzed(con, last_plant.id)
        con.commit()

# Run as a script
if __name__ == '__main__':
    main()
