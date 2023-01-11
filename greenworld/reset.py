# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import logging
import json
import schema
from schema import init_db, meta

def main():
    db = init_db()
    file = open('seed.json', 'r')
    data = json.load(file)
    logging.basicConfig(level=logging.NOTSET)
    with db.connect() as con:
        # Clear and recreate the database
        for table in reversed(meta.sorted_tables):
            try:
                con.execute(table.delete())
                logging.info(f'Dropped table {table}')
            except:
                logging.info(f'Skipped table {table}')
        meta.create_all(db)

        # Insert seed data from JSON
        for k, v in data.items():
            table = getattr(schema, f'{k}_table')
            for row in v:
                stmt = table.insert().values(**row)
                con.execute(stmt)

if __name__ == '__main__':
    main()