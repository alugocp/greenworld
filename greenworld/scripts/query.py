import sys
from sqlalchemy.orm import aliased
from greenworld.schema import (
    reports_table,
    plants_table,
    init_db
)

def main():
    db = init_db()
    with db.connect() as con:
        p1 = aliased(plants_table)
        p2 = aliased(plants_table)
        stmt = reports_table.select()\
            .with_only_columns(p1.c.name, p2.c.name, reports_table.c.report)\
            .join(p1, reports_table.c.plant1 == p1.c.id)\
            .join(p2, reports_table.c.plant2 == p2.c.id)
        result = con.execute(stmt)
        number = 1
        for row in result:
            sys.stdout.write(f'{number}) \033[4m{row[0]} x {row[1]}\033[0m\n')
            for a in row[2]:
                sys.stdout.write(f'• {a}\n')
            sys.stdout.write('\n')
            number += 1

if __name__ == '__main__':
    main()
