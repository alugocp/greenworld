# Drop the reports table from the database
# Clear the database save state table (which contains the last analyzed pair of plants)
from schema import (
    init_db,
    reports
)

def main():
    db = init_db()
    reports.drop(db)
    reports.create(db)

if __name__ == '__main__':
    main()