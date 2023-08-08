plant_field_labels = {
    'id': 'Greenworld ID',
    'family': 'Family',
    'growth_habit': 'Growth Habit',
    'fruit_weight': 'Fruit Weight',
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
    'family': '',
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

ecology_values = [
    'Negative allelopathic effect',
    'Positive allelopathic effect',
    'No allelopathic effect',
    'Pathogen',
    'Predator',
    'Seed disperser',
    'Pollinator'
]