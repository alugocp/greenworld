from urllib.parse import unquote_plus
import sqlalchemy
from flask import request
from greenworld import orm

def main(app, db):
    @app.route('/search/<prefix>')
    def plant_search_endpoint(prefix):
        prefix = unquote_plus(prefix)
        if len(prefix) < 3:
            return []
        with db.connect() as con:
            stmt = sqlalchemy.select(
                orm.plants_table.c.id,
                orm.plants_table.c.species,
                orm.plants_table.c.name) \
            .where(sqlalchemy.or_(
                orm.plants_table.c.species.like(f'{prefix}%'),
                orm.plants_table.c.name.like(f'{prefix}%')
            )) \
            .limit(10)
            return list(map(dict, con.execute(stmt).mappings().fetchall()))

    @app.route('/neighbors/<int:id_>')
    def grab_neighbors_endpoint(id_):
        stmt = sqlalchemy.select(
            orm.reports_table.c.plant1,
            orm.reports_table.c.plant2,
            orm.reports_table.c.score
        ).where(sqlalchemy.and_(
            sqlalchemy.or_(
                orm.reports_table.c.plant1 == id_,
                orm.reports_table.c.plant2 == id_,
            ),
            orm.reports_table.c.score != None
        )).order_by(orm.reports_table.c.score.desc()).limit(100)
        def remove_query_species(x):
            x = dict(x)
            score = None if x['score'] is None else float(x['score'])
            return [x['plant1'], score] if x['plant2'] == id_ else [x['plant2'], score]
        with db.connect() as con:
            return list(map(remove_query_species, con.execute(stmt).mappings().fetchall()))

    @app.route('/handlers')
    def grab_handlers_endpoint():
        if 'ids' not in request.args:
            return []
        ids = request.args.get('ids').split(',')
        stmt = sqlalchemy.select(
            orm.plants_table.c.id,
            orm.plants_table.c.species,
            orm.plants_table.c.name
        ).where(orm.plants_table.c.id.in_(ids))
        with db.connect() as con:
            return list(map(dict, con.execute(stmt).mappings().fetchall()))
