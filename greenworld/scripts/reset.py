# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import logging
import json
import copy
import sqlalchemy
import defs
import schema

def main():
    db = schema.init_db()
    with open('seed.json', 'r', encoding = 'utf-8') as file:
        data = json.load(file)
    logging.basicConfig(level=logging.NOTSET)
    with db.connect() as con:
        # Clear and recreate the database
        schema.meta.reflect(db)
        schema.meta.drop_all(db)
        logging.info('Dropped all existing tables')
        schema.meta.create_all(db)
        logging.info('Recreated new schema')

        # Insert seed data from JSON
        for k, v in data.items():
            table = getattr(schema, f'{k}_table')
            for row in v:
                values = copy.deepcopy(row)
                for col, val in values.items():
                    # Convert enum references to their integer values
                    if isinstance(table.c[col].type, sqlalchemy.Integer) and isinstance(val, str):
                        enum = val.split('.')
                        values[col] = getattr(defs, enum[0])[enum[1]].value
                stmt = table.insert().values(**values)
                logging.info(values)
                con.execute(stmt)

if __name__ == '__main__':
    main()
