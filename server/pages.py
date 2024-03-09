"""
This module registers page routes for the Flask app
"""

import copy
from urllib.parse import unquote_plus
import sqlalchemy
from flask import render_template
import lib
from greenworld import orm


def main(app, db):
    """
    Sets up page routes for the Flask app
    """

    @app.route("/")
    def homepage_endpoint():
        plant_stmt = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            orm.plants_table
        )
        report_stmt = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            orm.reports_table
        )
        with db.connect() as con:
            num_plants = con.execute(plant_stmt).fetchone()[0]
            num_reports = con.execute(report_stmt).fetchone()[0]
        return render_template(
            "homepage.html", num_plants=num_plants, num_reports=num_reports
        )

    @app.route("/plant/<species>")
    def plant_view_endpoint(species):
        species = unquote_plus(species)
        with db.connect() as con:
            stmt = orm.plants_table.select().where(
                orm.plants_table.c.species == species
            )
            plant = con.execute(stmt).mappings().fetchone()
            if plant:
                plant = lib.process_plant_dict(con, dict(plant))
                return render_template("plant.html", plant=plant)
        return render_template("404.html"), 404

    @app.route("/report/<species1>/<species2>")
    def report_view_endpoint(species1, species2):
        species1 = unquote_plus(species1)
        species2 = unquote_plus(species2)
        with db.connect() as con:
            stmt = orm.plants_table.select().where(
                orm.plants_table.c.species.in_([species1, species2])
            )
            plants = list(map(dict, con.execute(stmt).mappings().fetchall()))
            if len(plants) != 2:
                if species1 == species2:
                    plants.append(copy.deepcopy(plants[0]))
                else:
                    return render_template("404.html"), 404
            if plants[1]["id"] < plants[0]["id"]:
                plants = [plants[1], plants[0]]
            stmt = (
                orm.reports_table.select()
                .where(orm.reports_table.c.plant1 == plants[0]["id"])
                .where(orm.reports_table.c.plant2 == plants[1]["id"])
            )
            report = dict(con.execute(stmt).mappings().fetchone())
            if not report:
                return render_template("404.html"), 404
            for i, plant in enumerate(plants):
                plants[i] = lib.process_plant_dict(con, plant)
            return render_template(
                "report.html", report=report, plant1=plants[0], plant2=plants[1]
            )

    @app.route("/placement")
    def guild_placement_endpoint():
        return render_template("placement.html")

    @app.route("/companions")
    def companion_search_endpoint():
        return render_template("companions.html")

    @app.errorhandler(404)
    def not_found_endpoint(_):
        return render_template("404.html")
