import sys
import sqlalchemy
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db

# Expected clusters
GOOD = [
    ['zea mays', 'cucurbita maxima', 'phaseolus vulgaris']
]
BAD = [
    ['zea mays', 'solanum lycopersicum']
]

# Species companion data to add
'''
tomato
sweet potato
potato
broccoli
basil
garlic
onion
dill
fennel
watermelon
mint
kohlrabi
nasturtium
marigold
cucumber
cilantro
'''

# Generate report data
gw = Greenworld()
reset.main(gw, seed_data = False)
enter.main(gw, [
    'seed-data/pests.json',
    'seed-data/pathogens.json',
    'seed-data/three-sisters.json'
])
report.main(gw)

# Retrieve compatibility scores
plant_1_table = sqlalchemy.alias(plants_table)
plant_2_table = sqlalchemy.alias(plants_table)
stmt = sqlalchemy.select(
    reports_table.c.score,
    plant_1_table.c.species.label('species1'),
    plant_2_table.c.species.label('species2')
) \
.join(plant_1_table, reports_table.c.plant1 == plant_1_table.c.id) \
.join(plant_2_table, reports_table.c.plant2 == plant_2_table.c.id)

db = init_db()
with db.connect() as con:
    results = list(map(dict, con.execute(stmt).mappings().fetchall()))

# Create the distributions
neutral_dist = []
good_dist = []
bad_dist = []

def place_distribution(s1, s2, score):
    for g in GOOD:
        if s1 in g and s2 in g:
            good_dist.append(score)
            return
    for g in BAD:
        if s1 in g and s2 in g:
            bad_dist.append(score)
            return
    neutral_dist.append(score)

for r in results:
    place_distribution(r['species1'], r['species2'], float(r['score']))

# Statistical comparison between distributions
print(good_dist)
print(neutral_dist)
print(bad_dist)
# Show that each distribution is significantly different than the other two,
# and that good tends more towards -1.0 than neutral does, and that neutral
# tends more towards -1.0 than bad does.
