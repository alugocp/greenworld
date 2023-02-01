import greenworld.schema as schema
import greenworld.defs as defs
from sqlalchemy_utils import NumericRangeType
import sqlalchemy
import logging
import copy
import json
import sys
import os

# Conversions table for internal standard units
_conversions = {
  'f':   lambda f:   (f - 32) / 1.8,  # Convert to celsius
  'lbs': lambda lbs: lbs * 453.59237, # Convert to grams
  'in':  lambda x:   x * 0.0254,      # Convert to meters
  'ft':  lambda ft:  ft * 0.3048      # Convert to meters
}

# Prints helpful information to the terminal
def help():
  print(
    'Usage: python3 enter [file [...]]',
    'This command inserts all data from the given files to the Greenworld database, with the following rules:',
    ' • A JSON file must follow the structure defined in README.md',
    sep='\n'
  )

# Converts value from unit to the internal standard unit
def convert_to_unit(value):
  val, unit = value.split(' ')
  val = float(val)
  unit = unit.lower()
  if unit in ['m', 'g', 'c']:
    return val
  if unit not in _conversions:
    raise Exception(f'Unknown unit {unit}')
  return _conversions[unit](val)

# Process plant table bulk data entry
def enter_data(db, filename):
  _, ext = os.path.splitext(filename)
  if ext == '.json':
    return enter_data_json(db, filename)
  raise Exception(f'Data file with extension {ext} is not supported')

# Process plant table bulk data entry for a JSON file
def enter_data_json(db, filename):
  print('')
  logging.info(f'Writing data from {filename}')
  with open(filename, 'r', encoding = 'utf-8') as file:
    data = json.load(file)
  with db.connect() as con:
    for k in data.keys() | set(['plants', 'works_cited']):
      logging.info(f'Writing to {k} table')
      table = getattr(schema, f'{k}_table')
      for row in data[k]:
          values = copy.deepcopy(row)

          # Sanitize raw values for database
          for col, val in values.items():

              # Convert enum references to their integer values
              if isinstance(table.c[col].type, sqlalchemy.Integer) and isinstance(val, str):
                  enum = val.split('.')
                  values[col] = getattr(defs, enum[0])[enum[1]].value

              # Convert nonstandard units to internal standard units
              if isinstance(table.c[col].type, NumericRangeType) and isinstance(val[0], str):
                values[col][0] = convert_to_unit(val[0])
                values[col][1] = convert_to_unit(val[1])

          # Write sanitized values to database
          stmt = table.insert().values(**values)
          logging.info(values)
          con.execute(stmt)
      print('')
    con.commit()

def main(args):
  os.environ['GREENWORLD_DB'] = 'sqlite:///greenworld.db'
  logging.basicConfig(level=logging.NOTSET)
  db = schema.init_db()
  a = 0
  while a < len(args):
    if args[a] == '--help':
      help()
      break
    else:
      enter_data(db, args[a])
      a += 1

if __name__ == '__main__':
  main(sys.argv[1:])