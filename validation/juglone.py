import sys
import sqlalchemy
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db

# https://www.researchgate.net/publication/225979920_Allelopathy_in_black_walnut_Juglans_nigra_L_alley_cropping_I_Spatio-temporal_variation_in_soil_juglone_in_a_black_walnut-corn_Zea_mays_L_alley_cropping_system_in_the_midwestern_USA
# Allelopathy in black walnut (Juglans nigra L.) alley cropping. I. Spatio-temporal variation in soil juglone in a black walnut-corn (Zea mays L.) alley cropping system in the midwestern USA
# Jose & Gillespie, 1998
EXPECTED = 4.25

# Generate report data
gw = Greenworld()
reset.main(gw, seed_data = False)
enter.main(gw, ['seed-data/native-plants.json'])
report.main(gw)

# Retrieve reported distance
plant_1_table = sqlalchemy.alias(plants_table)
plant_2_table = sqlalchemy.alias(plants_table)
stmt = sqlalchemy.select(reports_table.c.range_union_min) \
.join(plant_1_table, reports_table.c.plant1 == plant_1_table.c.id) \
.join(plant_2_table, reports_table.c.plant2 == plant_2_table.c.id) \
.where(sqlalchemy.or_(
    sqlalchemy.and_(
        plant_1_table.c.species == 'juglans nigra',
        plant_2_table.c.species == 'allium tricoccum',
    ),
    sqlalchemy.and_(
        plant_2_table.c.species == 'juglans nigra',
        plant_1_table.c.species == 'allium tricoccum',
    )
))

db = init_db()
with db.connect() as con:
    result = float(con.execute(stmt).fetchone()[0])

# Calculate error value
error = (result - EXPECTED) / EXPECTED
# pylint: disable=consider-using-f-string
sys.stdout.write('\u001b[1mError:\u001b[0m \u001b[31m%s\u001b[0m%%\n' % (round(error * 100, 3)))
# pylint: enable=consider-using-f-string
