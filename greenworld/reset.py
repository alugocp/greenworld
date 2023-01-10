# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import json
import schema
from schema import init_db, meta

def main():
    db = init_db()
    file = open('seed.json', 'r')
    data = json.load(file)
    with db.connect() as con:
        # Clear and recreate the database
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        meta.create_all(db)

        # Insert seed data from JSON
        for k, v in data.items():
            table = getattr(schema, k)
            for row in v:
                stmt = table.insert().values(**row)
                con.execute(stmt)

if __name__ == '__main__':
    main()