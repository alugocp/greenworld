# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import logging
from greenworld.collection import iweb_xls
from greenworld.scripts import enter
from greenworld.lib import init_greenworld
from greenworld.lib import schema
from greenworld.lib import defs

def main():
    init_greenworld()
    db = schema.init_db()

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
        'seed-data/native-plants.json',
        'seed-data/pollinators.json'
    ])
    iweb_xls.main(
        '--citation = https://iwdb.nceas.ucsb.edu/html/clements_1923.html --col-headers = 4:100,1:2 --row-headers = 1:2,4:279 --range = 4:100,4:279 --map 1.0 POLLINATOR referenced-data/clements_1923.xls'.split(' ')
    )

if __name__ == '__main__':
    main()
