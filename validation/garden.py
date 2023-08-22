import sys
import sqlalchemy
import matplotlib.pyplot as plt
from scipy import stats
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db

# Expected companion results
GOOD = {
    'zea mays': [
        'cucurbita maxima',
        'phaseolus vulgaris'
    ],
    'cucurbita maxima': [
        'phaseolus vulgaris'
    ],
    'solanum lycopersicum': [
        'tagetes spp.',
        'tropaeolum majus',
        'coriandrum sativum',
        'helianthus annuus',
        'ocimum basilicum',
        'allium sativum'
    ],
    'ipomoea batatas': [
        'allium tricoccum',
        'allium cepa',
        'allium sativum',
        'anethum graveolens',
        'ocimum basilicum',
        'phaseolus vulgaris',
        'tagetes spp.',
        'tropaeolum majus'
    ],
    'solanum tuberosum': [
        'ocimum basilicum',
        'phaseolus vulgaris',
        'coriandrum sativum',
        'zea mays',
        'tagetes spp.',
        'tropaeolum majus'
    ],
    'brassica oleracea var. italica': [
        'allium tricoccum',
        'allium cepa',
        'allium sativum',
        'tropaeolum majus',
        'tagetes spp.',
        'anethum graveolens',
        'ocimum basilicum',
        'mentha spp.',
        'solanum tuberosum'
    ],
    'ocimum basilicum': [
        'coriandrum sativum',
        'tagetes spp.',
        'solanum lycopersicum',
        'solanum tuberosum'
    ]
}
BAD = {
    'zea mays': [
        'solanum lycopersicum'
    ],
    'solanum lycopersicum': [
        'brassica oleracea var. italica',
        'foeniculum vulgare',
        'anethum graveolens',
        'solanum tuberosum',
        'cucumis sativus',
        'zea mays'
    ],
    'ipomoea batatas': [
        'cucurbita maxima',
        'solanum lycopersicum',
        'helianthus annuus'
    ],
    'solanum tuberosum': [
        'cucumis sativus',
        'foeniculum vulgare',
        'allium cepa',
        'cucurbita maxima',
        'helianthus annuus',
        'solanum lycopersicum'
    ],
    'brassica oleracea var. italica': [
        'brassica oleracea var. gongylodes',
        'solanum lycopersicum',
        'cucurbita maxima'
    ],
    'ocimum basilicum': [
        'cucumis sativus',
        'foeniculum vulgare'
    ]
}

# Generate report data
gw = Greenworld('/dev/null')
reset.main(gw, seed_data = False)
enter.main(gw, [
    'seed-data/pests.json',
    'seed-data/pathogens.json',
    'seed-data/three-sisters.json',
    'seed-data/native-plants.json',
    'seed-data/garden.json'
])
report.main(gw)

# Double check the companion data species names
species_names = set()
for k in GOOD:
    species_names.add(k)
    for k1 in GOOD[k]:
        species_names.add(k1)

for k in BAD:
    species_names.add(k)
    for k1 in BAD[k]:
        species_names.add(k1)

db = init_db()
with db.connect() as con:
    db_species = con.execute(sqlalchemy.select(plants_table.c.species)).fetchall()

for name in species_names:
    if (name,) not in db_species:
        print(f'Unknown species "{name}"')
        sys.exit(1)

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

with db.connect() as con:
    results = list(map(dict, con.execute(stmt).mappings().fetchall()))

# Create the distributions
neutral_dist = []
good_dist = []
bad_dist = []
for r in results:
    if r['score'] is None:
        continue
    s1 = r['species1']
    s2 = r['species2']
    score = float(r['score'])
    if (s1 in GOOD and s2 in GOOD[s1]) or (s2 in GOOD and s1 in GOOD[s2]):
        good_dist.append(score)
    elif (s1 in BAD and s2 in BAD[s1]) or (s2 in BAD and s1 in BAD[s2]):
        bad_dist.append(score)
    elif (s1 in GOOD or s1 in BAD) and (s2 in GOOD or s2 in BAD):
        neutral_dist.append(score)

# Statistical comparison between distributions (Wilcoxon rank-sum tests)
sys.stdout.write('\u001b[1mp-values\u001b[0m\n')
sys.stdout.write('Good companions vs neutral: \u001b[31m%s\u001b[0m\n' % (stats.ranksums(good_dist, neutral_dist, alternative = 'greater').pvalue))
sys.stdout.write('Bad companions vs neutral: \u001b[31m%s\u001b[0m\n' % (stats.ranksums(bad_dist, neutral_dist, alternative = 'less').pvalue))

# Plot distributions and save to image
common = {
    'histtype': 'step',
    'bins': 100
}
plt.set_loglevel(level = 'warning')
plt.hist(good_dist, **common, color = 'green')
plt.hist(neutral_dist, **common, color = 'blue')
plt.hist(bad_dist, **common, color = 'red')
plt.savefig('validation/garden.png')

# Species companion data with references
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

https://borealbloomhomestead.com/basil-companion-plants/
Basil good: asparagus, borage, chamomile, cilantro, oregano, marigolds, peppers, radishes, carrots, turnips, beets, potatoes, tomatoes
Basil bad: cucumber, fennel, sage, rosemary

Garlic

Onion

Dill

Fennel

Watermelon

Mint

Kohlrabi

Nasturtium

Marigold

Cucumber

Cilantro
'''
