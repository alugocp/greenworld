from sqlalchemy.orm import aliased
from schema import (
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
        for row in result:
            print(f'{row[0]} x {row[1]}')
            for a in row[2]:
                print(f'• {a}')
            print('')

if __name__ == '__main__':
    main()
