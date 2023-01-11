# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import sqlalchemy
import logging
import json
import copy
import defs
import schema
from schema import init_db, meta

def main():
    db = init_db()
    file = open('seed.json', 'r')
    data = json.load(file)
    logging.basicConfig(level=logging.NOTSET)
    with db.connect() as con:
        # Clear and recreate the database
        meta.reflect(db)
        meta.drop_all(db)
        logging.info('Dropped all existing tables')
        meta.create_all(db)
        logging.info('Recreated new schema')

        # Insert seed data from JSON
        for k, v in data.items():
            table = getattr(schema, f'{k}_table')
            for row in v:
                values = copy.deepcopy(row)
                for col, val in values.items():
                    # Convert enum references to their integer values
                    if type(table.c[col].type) == sqlalchemy.Integer and type(val) == str:
                        enum = val.split('.')
                        values[col] = getattr(defs, enum[0])[enum[1]].value
                stmt = table.insert().values(**values)
                logging.info(values)
                con.execute(stmt)

if __name__ == '__main__':
    main()