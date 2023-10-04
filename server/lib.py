import re
from math import log
from intervals import DecimalInterval
import sqlalchemy
import consts
from greenworld import orm
from greenworld.serial import deserialize_enum_list


def citation_regex(href):
    return re.search(
        r"(?:[a-z]+://)(?:www\.)?([\w\d\-]+(\.[\w\d\-]+)*)/?", href
    ).groups()[0]


def process_plant_dict(con, plant):
    if "citations" in plant:
        ids = list(plant["citations"].keys())
        stmt = orm.works_cited_table.select().where(orm.works_cited_table.c.id.in_(ids))
        plant["citations"] = cite_fields(
            plant["citations"], list(con.execute(stmt).fetchall())
        )
    plant_id = plant["id"] if "id" in plant else 0
    plant = transform_plant(plant)
    plant["ecology"] = grab_ecology_data(con, plant_id)
    return plant


def transform_plant(plant):
    fields = []
    for k, label in consts.plant_field_labels.items():
        if plant[k] is None:
            value = "-"
        elif isinstance(plant[k], DecimalInterval):
            value = f"{plant[k].lower} - {plant[k].upper}"
        else:
            if k in ["id", "family"]:
                value = str(plant[k])
            elif k in ["soil", "drainage"]:
                indices = list(
                    map(lambda x: int(log(x) / log(2)), deserialize_enum_list(plant[k]))
                )
                value = ", ".join(list(map(lambda x: consts.plant_enum_values[k][x], indices)))
            else:
                value = consts.plant_enum_values[k][plant[k]]
            if k == "family":
                value = value.capitalize()
        field = "<td><b>" + label + "</b></td><td>" + value + "</td>"
        del plant[k]
        if k in plant["citations"]:
            citation = plant["citations"][k]
            citation_text = citation_regex(citation)
            field += f'<td><a href="{citation}">{citation_text}</a></td>'
        fields.append(field)
    plant["fields"] = fields
    return plant


def grab_ecology_data(con, plant_id):
    ecology = []

    # Aggregate non-plant ecological interactions
    stmt = (
        sqlalchemy.select(
            orm.other_species_table.c.name,
            orm.other_species_table.c.species,
            orm.ecology_other_table.c.relationship,
            orm.works_cited_table.c.citation,
        )
        .join(
            orm.other_species_table,
            orm.other_species_table.c.id == orm.ecology_other_table.c.non_plant,
        )
        .join(
            orm.works_cited_table,
            orm.works_cited_table.c.id == orm.ecology_other_table.c.citation,
        )
        .where(orm.ecology_other_table.c.plant == plant_id)
    )
    for row in con.execute(stmt).mappings():
        row = dict(row)
        row["relationship"] = consts.ecology_values[row["relationship"]]
        ecology.append(row)

    # Aggregate plant ecological interactions
    stmt = (
        sqlalchemy.select(
            orm.plants_table.c.name,
            orm.plants_table.c.species,
            orm.ecology_plant_table.c.relationship,
            orm.works_cited_table.c.citation,
        )
        .join(
            orm.plants_table, orm.plants_table.c.id == orm.ecology_plant_table.c.target
        )
        .join(
            orm.works_cited_table,
            orm.works_cited_table.c.id == orm.ecology_plant_table.c.citation,
        )
        .where(orm.ecology_plant_table.c.plant == plant_id)
    )
    for row in con.execute(stmt).mappings():
        row = dict(row)
        row["relationship"] = consts.ecology_values[row["relationship"]]
        ecology.append(row)
    return ecology


def cite_fields(citations, works_cited):
    new_citations = {}
    for k, v in citations.items():
        citation_link = next(x[1] for x in works_cited if str(x[0]) == k)
        for field in v:
            new_citations[field] = citation_link
    return new_citations
