from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.lib import Greenworld
from greenworld.lib.orm import reports_table
from greenworld.lib.orm import plants_table
from greenworld.lib.orm import init_db
import sqlalchemy
import sys

# https://www.nativeseeds.org/blogs/blog-news/how-to-grow-a-three-sisters-garden
control_matrices = [
    {
        'name': 'Three Sisters Mound',
        'zea mays': {
            'zea mays': 0.1524, # 6 inches as meters
            'phaseolus vulgaris': 0.0762, # 3 inches as meters
            'cucurbita maxima': 0.6096, # 24 inches as meters
        },
        'phaseolus vulgaris': {
            'phaseolus vulgaris': 0.26016307345234, # ((6 / √2) + 3) * √2 inches as meters
            'cucurbita maxima': 0.4762278984566999, # √((24 / √2)² + ((24 / √2) - 9)²) inches as meters
        },
        'cucurbita maxima': {
            'cucurbita maxima': 1.2192, # 48 inches as meters
        }
    },
    {
        'name': 'Three Sisters Field',
        'zea mays': {
            'zea mays': 0.3048, # 12 inches as meters
            'phaseolus vulgaris': 0.0762, # 3 inches as meters
            'cucurbita maxima': 0.9906 # 3 feet and 3 inches as meters
        },
        'phaseolus vulgaris': {
            'phaseolus vulgaris': 0.3048, # 12 inches as meters
            'cucurbita maxima': 0.9144 # 3 feet as meters
        },
        'cucurbita maxima': {
            'cucurbita maxima': 1.0668 # 3.5 feet as meters
        }
    },
    {
        'name': 'Three Sisters Landscape',
        'zea mays': {
            'zea mays': 0.3048, # 12 inches as meters
            'phaseolus vulgaris': 0.3048, # 12 inches as meters
            'cucurbita maxima': 0.9144 # 3 feet as meters
        },
        'phaseolus vulgaris': {
            'phaseolus vulgaris': 0.3048 # 12 inches as meters
        },
        'cucurbita maxima': {
            'cucurbita maxima': 0.9144 # 3 feet as meters
        }
    }
]

# Generate report data
gw = Greenworld()
reset.main(gw, seed_data = False)
enter.main(gw, [
    'seed-data/pests.json',
    'seed-data/pathogens.json',
    'seed-data/three-sisters.json'
])
report.main(gw)

# Query report data
plant_1_table = sqlalchemy.alias(plants_table)
plant_2_table = sqlalchemy.alias(plants_table)
stmt = sqlalchemy.select(
    reports_table.c.range_union_min,
    reports_table.c.range_union_max,
    plant_1_table.c.species.label('species1'),
    plant_2_table.c.species.label('species2')
) \
.join(plant_1_table, reports_table.c.plant1 == plant_1_table.c.id) \
.join(plant_2_table, reports_table.c.plant2 == plant_2_table.c.id)

db = init_db()
with db.connect() as con:
    results = list(map(dict, con.execute(stmt).mappings().fetchall()))
for r in results:
    r['range_union_max'] = float(r['range_union_max'])
    r['range_union_min'] = float(r['range_union_min'])

# Calculate error coefficients for each control matrix
sys.stdout.write('Error values (percentages) for traditional three sisters gardens\n')
for matrix in control_matrices:
    total_error = 0
    sys.stdout.write('\n\u001b[4m%s\u001b[0m\n' % (matrix['name']))
    n = 0
    for r in results:
        error = 0
        try:
            value = matrix[r['species1']][r['species2']] if r['species2'] in matrix[r['species1']] else matrix[r['species2']][r['species1']]
        except:
            continue
        if value > r['range_union_max']:
            error = (r['range_union_max'] - value) / value
        elif value < r['range_union_min']:
            error = (r['range_union_min'] - value) / value
        sys.stdout.write('%s x %s: \u001b[31m%s \u001b[0m\n' % (r['species1'], r['species2'], round(error * 100, 3)))
        total_error += abs(error)
        n += 1
    sys.stdout.write('\u001b[1mTotal error:\u001b[0m \u001b[31m%s\u001b[0m\n' % (round(total_error * 100, 3)))
    sys.stdout.write('\u001b[1mAverage error:\u001b[0m \u001b[31m%s\u001b[0m\n' % (round(total_error * 100 / n, 3)))
