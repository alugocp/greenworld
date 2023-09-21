import sys
import json
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

# Potential sources of error:
#  - Certain good or bad pairs are missing from this data set
#  - Plant data is missing or inaccurate
#  - The algorithm needs tweaks

# Tested species list
# Corn - zea mays
# Squash - cucurbita maxima
# Beans - phaseolus vulgaris
# Sunflower - helianthus annuus
# Ramps - allium tricoccum
# Groundnut - apios americana
# Tomato - solanum lycopersicum
# Sweet potato - ipomoea batatas
# Potato - solanum tuberosum
# Broccoli - brassica oleracea var. italica
# Basil - ocimum basilicum
# Garlic - allium sativum
# Onion - allium cepa
# Dill - anethum graveolens
# Fennel - foeniculum vulgare
# Watermelon - citrullus lanatus
# Mint - mentha spp.
# Kohlrabi - brassica oleracea var. gongylodes
# Nasturtium - tropaeolum majus
# Marigold - tagetes spp.
# Cucumber - cucumis sativus
# Cilantro - coriandrum sativum

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
    ],
    'allium sativum': [
        'anethum graveolens',
        'solanum lycopersicum',
        'solanum tuberosum',
        'brassica oleracea var. italica',
        'brassica oleracea var. gongylodes',
        'tropaeolum majus',
        'tagetes spp.'
    ],
    'allium cepa': [
        'allium cepa',
        'allium sativum',
        'allium tricoccum',
        'brassica oleracea var. italica',
        'brassica oleracea var. gongylodes',
        'solanum lycopersicum',
        'solanum tuberosum',
        'anethum graveolens',
        'tagetes spp.'
    ],
    'anethum graveolens': [
        'zea mays',
        'cucumis sativus',
        'allium cepa',
        'brassica oleracea var. italica',
        'brassica oleracea var. gongylodes'
    ],
    'foeniculum vulgare': [
        'anethum graveolens',
        'cucumis sativus'
    ],
    'citrullus lanatus': [
        'zea mays',
        'phaseolus vulgaris',
        'anethum graveolens',
        'tagetes spp.',
        'tropaeolum majus',
        'allium sativum',
        'mentha spp.',
        'brassica oleracea var. italica'
    ],
    'mentha spp.': [
        'cucurbita maxima',
        'brassica oleracea var. italica',
        'allium cepa',
        'phaseolus vulgaris',
        'solanum lycopersicum',
        'tagetes spp.'
    ],
    'brassica oleracea var. gongylodes': [
        'phaseolus vulgaris',
        'cucumis sativus',
        'allium cepa',
        'solanum tuberosum'
    ],
    'tropaeolum majus': [
        'phaseolus vulgaris',
        'cucumis sativus',
        'cucurbita maxima',
        'brassica oleracea var. italica'
    ],
    'tagetes spp.': [
        'cucumis sativus',
        'cucurbita maxima',
        'citrullus lanatus',
        'solanum lycopersicum',
        'solanum tuberosum',
        'phaseolus vulgaris',
        'brassica oleracea var. italica',
        'allium cepa'
    ],
    'cucumis sativus': [
        'phaseolus vulgaris',
        'zea mays',
        'anethum graveolens',
        'tropaeolum majus',
        'tagetes spp.',
        'helianthus annuus',
        'allium sativum',
        'apios americana'
    ],
    'coriandrum sativum': [
        'phaseolus vulgaris',
        'apios americana',
        'helianthus annuus'
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
    ],
    'allium sativum': [
        'phaseolus vulgaris'
    ],
    'allium cepa': [
        'phaseolus vulgaris'
    ],
    'foeniculum vulgare': [
        'phaseolus vulgaris',
        'solanum lycopersicum',
        'solanum tuberosum'
    ],
    'citrullus lanatus': [
        'solanum tuberosum',
        'cucurbita maxima',
        'cucumis sativus'
    ],
    'brassica oleracea var. gongylodes': [
        'brassica oleracea var. gongylodes',
        'brassica oleracea var. italica',
        'solanum lycopersicum'
    ],
    'tropaeolum majus': [
        'mentha spp.',
        'solanum lycopersicum'
    ],
    'cucumis sativus': [
        'mentha spp.',
        'solanum tuberosum',
        'citrullus lanatus',
        'foeniculum vulgare'
    ],
    'coriandrum sativum': [
        'foeniculum vulgare'
    ]
}

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

# Double check the companion data species names
species_names = set()
for k, v in GOOD.items():
    species_names.add(k)
    for k1 in v:
        species_names.add(k1)

for k, v in BAD.items():
    species_names.add(k)
    for k1 in v:
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
    reports_table.c.report,
    plant_1_table.c.species.label('species1'),
    plant_2_table.c.species.label('species2')
) \
.join(plant_1_table, reports_table.c.plant1 == plant_1_table.c.id) \
.join(plant_2_table, reports_table.c.plant2 == plant_2_table.c.id) \
.where(reports_table.c.score is not None)

with db.connect() as con:
    results = list(map(dict, con.execute(stmt).mappings().fetchall()))

# Create the distributions and reports
neutral_reports = []
neutral_dist = []
good_reports = []
good_dist = []
bad_reports = []
bad_dist = []
for r in results:
    r['score'] = float(r['score'])
    s1 = r['species1']
    s2 = r['species2']
    score = float(r['score'])
    if (s1 in GOOD and s2 in GOOD[s1]) or (s2 in GOOD and s1 in GOOD[s2]):
        good_dist.append(score)
        good_reports.append(r)
    elif (s1 in BAD and s2 in BAD[s1]) or (s2 in BAD and s1 in BAD[s2]):
        bad_dist.append(score)
        bad_reports.append(r)
    elif (s1 in GOOD or s1 in BAD) and (s2 in GOOD or s2 in BAD):
        neutral_dist.append(score)
        neutral_reports.append(r)

# Write report files
with open('validation/garden-neutral-reports.txt', 'w', encoding = 'utf-8') as file:
    file.write(json.dumps(neutral_reports, indent = 4))
with open('validation/garden-good-reports.txt', 'w', encoding = 'utf-8') as file:
    file.write(json.dumps(good_reports, indent = 4))
with open('validation/garden-bad-reports.txt', 'w', encoding = 'utf-8') as file:
    file.write(json.dumps(bad_reports, indent = 4))

# Percentage of "good" identified companions within a distribution
def percent_good(dist):
    percent = len(list(filter(lambda x: x <= 0, dist))) / len(dist)
    return round(percent * 10000) / 100

# Statistical comparison between distributions (Wilcoxon rank-sum tests)
# pylint: disable=consider-using-f-string
sys.stdout.write('\u001b[1mp-values\u001b[0m\n')
sys.stdout.write('Good companions vs neutral: \u001b[31m%s\u001b[0m\n' % (stats.ranksums(good_dist, neutral_dist, alternative = 'greater').pvalue))
sys.stdout.write('Bad companions vs neutral: \u001b[31m%s\u001b[0m\n' % (stats.ranksums(bad_dist, neutral_dist, alternative = 'less').pvalue))
sys.stdout.write('Bad companions vs good: \u001b[31m%s\u001b[0m\n' % (stats.ranksums(bad_dist, good_dist, alternative = 'less').pvalue))
sys.stdout.write('Good companions percentage of good companions: \u001b[31m%s\u001b[0m%%\n' % (percent_good(good_dist)))
sys.stdout.write('Good companions percentage of neutral companions: \u001b[31m%s\u001b[0m%%\n' % (percent_good(neutral_dist)))
sys.stdout.write('Good companions percentage of bad companions: \u001b[31m%s\u001b[0m%%\n' % (percent_good(bad_dist)))
# pylint: enable=consider-using-f-string

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
# pylint: disable=pointless-string-statement
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

https://www.gardeningknowhow.com/edible/herbs/garlic/companions-for-garlic.htm
Garlic good: Dill, Beets, Kale, Spinach, Potatoes, Carrots, Eggplants, Tomatoes, Peppers, Cabbage, Cauliflower, Broccoli, Kohlrabi, Roses, Geraniums, Marigolds, Nasturtiums
Garlic bad: asparagus, peas, beans, sage, parsley

https://www.thespruce.com/onion-companion-plants-7368901
Onion good: beets, spinach, alliums, brassicas, tomatoes, peppers, eggplant, strawberries, potatoes, lettuce, parsnips, carrots, chamomile, parsley, dill, savory, marigolds, roses
Onion bad: peas, beans, asparagus, sage

https://www.gardeningknowhow.com/edible/herbs/dill/dill-companion-plants.htm
Dill good: Asparagus, Corn, Cucumbers, Onion, Lettuce, Brassicas, Basil
Dill bad: Carrot

https://plantura.garden/uk/vegetables/fennel/planting-fennel
Fennel good: Peas, Lettuce, Cucumber, Sage
Fennel bad: Nightshades, Beans

https://www.thespruce.com/companion-plants-for-watermelons-5069542
Watermelon good: Garlic, Catnip, Dill, Mint, Nasturtiums, Corn, Broccoli, Radishes, Tansies, Marigold, Lavender, Borage, Beans
Watermelon bad: Cucumbers, Summer squash/zucchini, Pumpkins, Winter squash, Potato

https://www.gardenia.net/guide/best-worst-companions-for-mint
Mint good: onion, beet, cauliflower, cabbage, broccoli, pumpkin, zucchini, carrot, lettuce, pea, radish, tomato, eggplant, beans, corn, marigold
Mint bad: chamomile, oregano, parsley, rosemary

https://www.gardeningknowhow.com/edible/vegetables/kohlrabi/kohlrabi-companion-plants.htm
Kohlrabi good: Bush beans, Beets, Celery, Cucumbers, Lettuce, Onions, Potatoes
Kohlrabi bad: Brassicas, Tomatoes

https://garden-housing.com/gardening/nasturtium-companion-plants/
Nasturtium good: Beans, Broccoli, Cabbage, Cucumber, Radish, Squash, Strawberry
Nasturtium bad: Mint, Sage, Thyme, Tomato

https://www.bunnysgarden.com/marigold-companion-plants/
Marigold good: Asparagus, Basil, Beans, Broccoli, Cabbage, Cucumbers, Eggplant, Gourds, Kale, Lettuce, Melons, Onions, Peppers, Potatoes, Pumpkins, Radish, Squash, Tomatoes
Marigold bad: N/A

https://www.thespruce.com/companion-plants-for-cucumbers-2540044
Cucumber good: legumes, corn, radishes, beets, carrots, garlic, marigolds, nasturtiums, sunflowers, dill, oregano
Cucumber bad: potatoes, sage, mint, melon, fennel

https://www.thespruce.com/companion-plants-for-cilantro-5074346
Cilantro good: Chervil, Sweet alyssum, Coreopsis, Legumes, Cosmos, Zinnias, Sunflowers
Cilantro bad: Lavender, Thyme, Rosemary, Fennel
'''
# pylint: enable=pointless-string-statement
