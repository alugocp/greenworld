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
https://www.thespruce.com/companion-plants-for-tomatoes-1403289
Tomato good: calendula, chives, black-eyed peas, radishes, sage, french marigold, nasturtium, cilantro, oregano, parsley, crimson clover, lavendar, sunflower, zinnia, asparagus, basil, borage, carrot, garlic, sweet allysum, thyme
Tomato bad: Broccoli (any brassicaceae species), Fennel, Dill, Potato (any solanaceae species), Cucumbers, Corn, Rosemary

https://borealbloomhomestead.com/sweet-potato-companion-plants/#best-sweet-potato-companion-plants
Sweet potato good: alliums, allysum, thyme, dill, basil, legumes, marigolds, nasturtium, radishes, spinach, yarrow
Sweet potato bad: squash, tomato, sunflower

https://www.thespruce.com/companion-plants-for-potatoes-2540039
Potato good: Alyssum, Basil, Beans, Cabbage, Catnip, Chamomile, Coriander, Corn, Horseradish, Lettuce, Marigolds, Nasturtium, Parsley, Peas, Petunias, Radishes, Scallions, Spinach, Tansy, Thyme, Yarrow
Potato bad: Carrots, Cucumbers, Eggplant, Fennel, Okra, Onions, Peppers, Pumpkins, Raspberries, Squash, Sunflowers, Tomatoes, Tomatillos, Turnips

https://borealbloomhomestead.com/broccoli-companion-plants/
Broccoli good: alliums, beets, celery, nasturtiums, french marigolds, dill ,basil, mint, chamomile, rosemary, lettuce, spinach, potato
Broccoli bad: brassica species, strawberries, tomato, peppers, pumpkin
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
