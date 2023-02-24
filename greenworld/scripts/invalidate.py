# Drop the reports table from the database.
# Clear the database save state table (which contains the last analyzed pair of plants).
from greenworld.lib import Greenworld
from greenworld.lib.orm import (
    init_db,
    reports_table,
    memory_table
)

def main(gw: Greenworld):
    db = init_db()
    reports_table.drop(db)
    reports_table.create(db)
    with db.connect() as con:
        con.execute(memory_table.delete())
        con.commit()
    gw.log('Reports data has been wiped')

if __name__ == '__main__':
    main(Greenworld())
