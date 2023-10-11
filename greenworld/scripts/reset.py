"""
This script hard resets the local database used in this project.
It then repopulates the database from the `seed.json` file.
"""
from greenworld.scripts import collect
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld import orm
from greenworld import defs


def main(gw: Greenworld, seed_data=False):
    """
    Script entry point
    """
    db = orm.init_db()

    # Clear and recreate the database
    orm.meta.reflect(db)
    orm.meta.drop_all(db)
    gw.log("Dropped all existing tables")
    orm.meta.create_all(db)
    gw.log("Recreated new schema")

    # Set a plant kingdom value in the other_species table
    with db.connect() as con:
        stmt = orm.other_species_table.insert().values(
            id=defs.PLANTAE, species="Plantae", name="Plant Kingdom"
        )
        con.execute(stmt)
        con.commit()

    # Seed the database
    if seed_data:
        collect.main(gw, ["referenced-data/clements_1923.xls"])
        enter.main(
            gw,
            [
                "seed-data/tmp0.json",
                "seed-data/pests.json",
                "seed-data/pathogens.json",
                "seed-data/pollinators.json",
                "seed-data/three-sisters.json",
                "seed-data/native-plants.json",
                "seed-data/garden.json",
            ],
        )


if __name__ == "__main__":
    main(Greenworld(), seed_data=True)
