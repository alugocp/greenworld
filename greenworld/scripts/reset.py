# This script hard resets the local database used in this project.
# It then repopulates the database from the `seed.json` file.
import logging
from greenworld import schema
from greenworld.scripts import enter

def main():
    db = schema.init_db()
    logging.basicConfig(level = logging.NOTSET)

    # Clear and recreate the database
    schema.meta.reflect(db)
    schema.meta.drop_all(db)
    logging.info('Dropped all existing tables')
    schema.meta.create_all(db)
    logging.info('Recreated new schema')

    # Seed the database
    enter.main([
        'seed-data/three-sisters.json',
        'seed-data/native-plants.json'
    ])

if __name__ == '__main__':
    main()
