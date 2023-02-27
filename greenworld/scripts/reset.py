# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
from greenworld.collection import iweb_xls_script
from greenworld.scripts import enter
from greenworld.lib import Greenworld
from greenworld.lib import orm
from greenworld.lib import defs

def main(gw: Greenworld, seed_data = False):
    db = orm.init_db()

    # Clear and recreate the database
    orm.meta.reflect(db)
    orm.meta.drop_all(db)
    gw.log('Dropped all existing tables')
    orm.meta.create_all(db)
    gw.log('Recreated new schema')

    # Set a plant kingdom value in the other_species table
    with db.connect() as con:
        stmt = orm.other_species_table.insert().values(
            id = defs.PLANTAE,
            species = 'plantae',
            name = 'Plant Kingdom'
        )
        con.execute(stmt)
        con.commit()

    # Seed the database
    if seed_data:
        enter.main(gw, [
            'seed-data/three-sisters.json',
            'seed-data/native-plants.json',
            'seed-data/pollinators.json'
        ])
        iweb_xls_script.main(
            gw,
            '--citation = https://iwdb.nceas.ucsb.edu/html/clements_1923.html --col-headers = 4:100,1:2 --row-headers = 1:2,4:279 --range = 4:100,4:279 --map 1.0 POLLINATOR referenced-data/clements_1923.xls'.split(' ')
        )

if __name__ == '__main__':
    main(Greenworld(), seed_data = True)
