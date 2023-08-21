import sys
import sqlalchemy
import matplotlib.pyplot as plt
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db

# Species to internal names
names_map = {
    'zea mays': 'corn',
    'cucurbita maxima': 'squash',
    'phaseolus vulgaris': 'beans',
    'helianthus annuus': 'sunflower',
    'solanum lycopersicum': 'tomato',
    'ipomoea batatas': 'sweet potato',
    'solanum tuberosum': 'potato',
    'brassica oleracea var. italica': 'broccoli',
    'ocimum basilicum': 'basil',
    'allium sativum': 'garlic',
    'allium cepa': 'onion',
    'anethum graveolens': 'dill',
    'foeniculum vulgare': 'fennel',
    'citrullus lanatus': 'watermelon',
    'mentha spp.': 'mint',
    'brassica oleracea var. gongylodes': 'kohlrabi',
    'tropaeolum majus': 'nasturtium',
    'tagetes spp.': 'marigold',
    'cucumis sativus': 'cucumber',
    'coriandrum sativum': 'cilantro',
    'allium tricoccum': 'ramps'
}

# Expected clusters
GOOD = {
    'corn': ['squash', 'beans'],
    'squash': ['beans'],
    'tomato': ['marigold', 'nasturtium', 'cilantro', 'sumflower', 'basil', 'garlic'],
    'sweet potato': ['ramps', 'onion', 'garlic', 'dill', 'basil', 'beans', 'marigold', 'nasturtium'],
    'potato': ['basil', 'beans', 'cilantro', 'corn', 'marigold', 'nasturtium'],
    'broccoli': ['ramps', 'onion', 'garlic', 'nasturtium', 'marigold', 'dill', 'basil', 'mint', 'potato'],
}
BAD = {
    'corn': ['tomato'],
    'tomato': ['broccoli', 'fennel', 'dill', 'potato', 'cucumber', 'corn'],
    'sweet potato': ['squash', 'tomato', 'sunflower'],
    'potato': ['cucumber', 'fennel', 'onion', 'squash', 'sunflower', 'tomato'],
    'broccoli': ['kohlrabi', 'tomato', 'squash']
}

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
Broccoli good: alliums, beets, celery, nasturtiums, french marigolds, dill, basil, mint, chamomile, rosemary, lettuce, spinach, potato
Broccoli bad: brassica species, strawberries, tomato, peppers, pumpkin
'''

# Generate report data
gw = Greenworld()
reset.main(gw, seed_data = False)
enter.main(gw, [
    'seed-data/pests.json',
    'seed-data/pathogens.json',
    'seed-data/three-sisters.json',
    'seed-data/native-plants.json',
    'seed-data/garden.json'
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
    if (s1 in GOOD and s2 in GOOD[s1]) or (s2 in GOOD and s1 in GOOD[s2]):
        good_dist.append(score)
        return
    if (s1 in BAD and s2 in BAD[s1]) or (s2 in BAD and s1 in BAD[s2]):
        bad_dist.append(score)
        return
    neutral_dist.append(score)

for r in results:
    if r['species1'] in names_map and r['species2'] in names_map:
        place_distribution(names_map[r['species1']], names_map[r['species2']], float(r['score']))

# Statistical comparison between distributions

# Show that each distribution is significantly different than the other two,
# and that good tends more towards -1.0 than neutral does, and that neutral
# tends more towards -1.0 than bad does.

# Plot distributions and save to image
common = {
    'histtype': 'step',
    'bins': 100
}
plt.hist(good_dist, **common, color = 'green')
plt.hist(neutral_dist, **common, color = 'blue')
plt.hist(bad_dist, **common, color = 'red')
plt.savefig('validation/garden.png')
