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

    @app.route('/reports')
    def grab_reports_endpoint():
        if 'species_list' not in request.args:
            return []
        species_list = request.args.get('species_list').split(',')
        stmt = orm.reports_table.select() \
        .where(sqlalchemy.or_(
            orm.reports_table.c.plant1.in_(species_list),
            orm.reports_table.c.plant2.in_(species_list)
        ))
        with db.connect() as con:
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
        )).order_by(orm.reports_table.c.score).limit(100)
        def remove_query_species(x):
            x = dict(x)
            return [x['plant1'], x['score']] if x['plant2'] == id_ else [x['plant2'], x['score']]
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
