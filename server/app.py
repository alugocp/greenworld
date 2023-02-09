import os
import sys
from urllib.parse import unquote_plus
from intervals import DecimalInterval
from flask import (
    Flask,
    render_template
)
sys.path.append('.')
from greenworld import schema
app = Flask(
    'Greenworld',
    template_folder = 'server/templates'
)
os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
db = schema.init_db()

# Helpful values
plant_field_labels = {
    'id': 'Internal ID',
    'growth_habit': 'Growth Habit',
    'height': 'Height',
    'spread': 'Spread',
    'length': 'Length',
    'root_spread': 'Root Spread',
    'root_depth': 'Root Depth',
    'nitrogen': 'Nitrogen',
    'temperature': 'Temperature',
    'sun': 'Sun',
    'soil': 'Soil Type',
    'pH': 'pH',
    'drainage': 'Soil Drainage'
}

plant_field_units = {
    'fruit_weight': 'g',
    'height': 'm',
    'spread': 'm',
    'length': 'm',
    'root_spread': 'm',
    'root_depth': 'm',
    'temperature': '° C',
    'pH': ''
}

plant_enum_values = {
    'growth_habit': ['Forb', 'Graminoid', 'Lichenous', 'Nonvascular', 'Shrub', 'Subshrub', 'Tree', 'Vine'],
    'nitrogen': ['Nitrogen fixer', 'Standard feeder', 'Heavy feeder'],
    'sun': ['Full shade', 'Partial sun', 'Full sun'],
    'soil': ['Sand', 'Clay', 'Silt', 'Loam'],
    'drainage': [
        'Very poorly drained',
        'Poorly drained',
        'Somewhat poorly drained',
        'Moderately well drained',
        'Well drained',
        'Somewhat excessively drained',
        'Excessively drained'
    ]
}

def transform_plant(plant):
    fields = []
    for k, label in plant_field_labels.items():
        if plant[k] is None:
            value = '-'
        elif isinstance(plant[k], DecimalInterval):
            value = f'{plant[k].lower}{plant_field_units[k]} - {plant[k].upper}{plant_field_units[k]}'
        else:
            if k == 'id':
                value = str(plant[k])
            else:
                value = plant_enum_values[k][plant[k]]
        fields.append('<b>' + label + ':</b> ' + value)
    plant['fields'] = fields
    return plant

@app.route('/')
def homepage_endpoint():
    return render_template('homepage.html')

@app.route('/plant/<species>')
def plant_view_endpoint(species):
    species = unquote_plus(species)
    with db.connect() as con:
        stmt = schema.plants_table.select().where(schema.plants_table.c['species'] == species)
        plant = con.execute(stmt).mappings().fetchone()
    if plant:
        return render_template('plant.html', plant = transform_plant(dict(plant)))
    return f'Plant \'{species}\' not found', 404

if __name__ == '__main__':
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(port = 2017)
