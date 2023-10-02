# This script generates compatibility reports for newly added plants in the database.
# It does this in the following order:
# • Go through each pair of plants starting at the last analyzed pair
# • Run algorithm modules on them by a database check
# • Write the report back to the database
import sqlalchemy
from greenworld.serial import serialize_factors
from greenworld.algorithm import GreenworldAlgorithm
from greenworld import Greenworld
from greenworld.orm import (
    MAX_PLANTING_RANGE,
    init_db,
    reports_table,
    memory_table,
    plants_table
)

# Retrieves the highest plant ID in the database
def get_last_plant(con):
    stmt = sqlalchemy.select(plants_table.c.id).order_by(plants_table.c.id.desc()).limit(1)
    result = con.execute(stmt).fetchone()
    return result[0] if result else 0

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

# Calculates the accumulated suggested range from this report
def get_range_union(report):
    max_dist = MAX_PLANTING_RANGE
    min_dist = 0
    for factor in report:
        if factor.interval:
            dist1, dist2 = factor.interval
            if dist1 > min_dist:
                min_dist = dist1
                max_dist = dist2
    for factor in report:
        if factor.interval:
            _, dist2 = factor.interval
            if min_dist < dist2 < max_dist:
                max_dist = dist2
    return min_dist, max_dist

# Checks if the report has enough information to provide a compatibility score
def is_valid_report(report):
    if report is not None:
        for factor in report:
            if factor.interval is not None:
                return True
    return False

# Calculate the overall compatibility score
def calculate_compatibility_score(x, plant1, plant2):
    if plant1.spread and plant2.spread:
        return (2 * x / float(plant1.spread.lower + plant2.spread.lower)) - 1
    return None

# Calculates how many reports will be needed given the number of old and new plants
def get_analysis_total(num_new, num_old):
    return int(((num_new + 1) * (num_new / 2)) + (num_new * num_old))

# The main loop for companionship reporting
def main(gw: Greenworld):
    db = init_db()
    algorithm = GreenworldAlgorithm()
    with db.connect() as con:
        last_plant = None
        last_analyzed = get_last_analyzed(con)
        number_plants = get_last_plant(con)
        analysis_current = 0
        analysis_total = get_analysis_total(number_plants - last_analyzed, last_analyzed)
        for plant1 in get_plants(con, plants_table.c.id > last_analyzed).mappings():
            for plant2 in get_plants(con, plants_table.c.id <= plant1.id).mappings():
                analysis_current += 1
                gw.log(f'{analysis_current}/{analysis_total}: {plant2.name} ({plant2.species}) x {plant1.name} ({plant1.species})')
                report = algorithm.generate_report(con, plant1, plant2)
                con.execute(reports_table.insert().values(
                    plant1 = plant2.id,
                    plant2 = plant1.id,
                    score = report.score,
                    range_union_min = 0,
                    range_union_max = 0,
                    report = serialize_factors(report.factors)
                ))
            last_plant = plant1
        if last_plant:
            set_last_analyzed(con, last_plant.id)
        con.commit()

# Run as a script
if __name__ == '__main__':
    main(Greenworld())
