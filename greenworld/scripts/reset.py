# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import logging
from greenworld.scripts import enter
from greenworld import schema
from greenworld import defs

def main():
    db = schema.init_db()
    logging.basicConfig(level = logging.NOTSET)

    # Clear and recreate the database
    schema.meta.reflect(db)
    schema.meta.drop_all(db)
    logging.info('Dropped all existing tables')
    schema.meta.create_all(db)
    logging.info('Recreated new schema')

    # Set a plant kingdom value in the other_species table
    with db.connect() as con:
        stmt = schema.other_species_table.insert().values(
            id = defs.PLANTAE,
            species = 'plantae',
            name = 'Plant kingdom'
        )
        con.execute(stmt)
        con.commit()

    # Seed the database
    enter.main([
        'seed-data/three-sisters.json',
        'seed-data/native-plants.json'
    ])

if __name__ == '__main__':
    main()
