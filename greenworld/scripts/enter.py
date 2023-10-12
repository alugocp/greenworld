import copy
import json
import sys
import sqlalchemy
from greenworld.schema import json_schema
from greenworld.taxonomy import Taxon
from greenworld import Greenworld
from greenworld import orm
from greenworld import defs


# Prints helpful information to the terminal
def print_help():
    print(
        "Usage: python3 enter [file [...]]",
        "This command inserts all data from the given JSON file(s) into the Greenworld database.",
        "Each file must follow the structure defined in README.md",
        sep="\n",
    )


# Returns the last ID from a table
def get_last_id(con, table):
    return (
        con.execute(table.select().order_by(table.c.id.desc()).limit(1))
        .mappings()
        .fetchone()
        or {"id": 0}
    )["id"]


# Returns a row from some table where one column equals a given value
def select_by(con, table, column, value):
    return (
        con.execute(table.select().where(table.c[column] == value))
        .mappings()
        .fetchone()
    )


# Parses a string representing an enum into its integer value
def parse_enum(name):
    enum = name.split(".")
    try:
        return getattr(defs, enum[0])[enum[1]].value
    except Exception as e:
        raise ValueError(f"Unknown enum '{name}'") from e


# Parses a list of enums into their summation value
def parse_enum_range(enums):
    sum_total = 0
    for name in enums:
        sum_total += parse_enum(name)
    return sum_total


# Process plant table bulk data entry for a JSON file
def enter_data(gw: Greenworld, db, data):
    assert json_schema.validate(data) == data
    taxon = Taxon()

    with db.connect() as con:
        works_cited_map = get_works_cited_map(gw, con, data)

        # Write other species data to the database
        gw.log("Writing other species data...")
        last_other_id = get_last_id(con, orm.other_species_table)
        for row in data["others"] if "others" in data else []:
            values = copy.deepcopy(row)
            values["species"] = taxon.parse(values["species"]).format()
            if "family" in values:
                values["family"] = Taxon.family(values["family"])
            result = select_by(
                con, orm.other_species_table, "species", values["species"]
            )
            if result:
                new_values = {}
                new_values.update(result)
                new_values.update(values)
                gw.log(f"UPDATE {new_values}")
                con.execute(
                    orm.other_species_table.update()
                    .where(orm.other_species_table.c["id"] == result["id"])
                    .values(**new_values)
                )
            else:
                values["id"] = last_other_id + 1
                last_other_id += 1
                gw.log(f"INSERT {values}")
                con.execute(orm.other_species_table.insert().values(**values))
        gw.log("")

        # Sanitize and write plant data to database
        ecology_data = {}
        gw.log("Writing plant and interaction data...")
        last_plant_id = get_last_id(con, orm.plants_table)
        for row in data["plants"] if "plants" in data else []:
            values = copy.deepcopy(row)
            values["species"] = taxon.parse(values["species"]).format()
            values["family"] = Taxon.family(values["family"])
            del values["id"]
            local_ecology_data = values.pop("ecology") if "ecology" in values else []

            # Map citations
            mapped_citations = {}
            for cite_key in (values["citations"] or {}).keys():
                mapped_citations[str(works_cited_map[int(cite_key)])] = values[
                    "citations"
                ][cite_key]
            values["citations"] = mapped_citations

            # Map general properties of plant data
            for col, val in values.items():
                # Convert singular enum references to their integer values
                if isinstance(
                    orm.plants_table.c[col].type, sqlalchemy.Integer
                ) and isinstance(val, str):
                    values[col] = parse_enum(val)

                # Convert multiple enum references to their summed integer values
                if isinstance(
                    orm.plants_table.c[col].type, sqlalchemy.Integer
                ) and isinstance(val, list):
                    values[col] = parse_enum_range(val)

            # Write sanitized values to database
            result = select_by(con, orm.plants_table, "species", values["species"])
            if result:
                new_values = {}
                new_values.update(result)
                new_values.update(values)
                ecology_data[result["id"]] = local_ecology_data
                gw.log(f"UPDATE {new_values}")
                con.execute(
                    orm.plants_table.update()
                    .where(orm.plants_table.c["id"] == result["id"])
                    .values(**new_values)
                )
            else:
                values["id"] = last_plant_id + 1
                last_plant_id += 1
                ecology_data[values["id"]] = local_ecology_data
                gw.log(f"INSERT {values}")
                con.execute(orm.plants_table.insert().values(**values))

        # Handle ecological data
        for plant_id, ecology_data_entry in ecology_data.items():
            process_ecological_fields(gw, con, works_cited_map, plant_id, ecology_data_entry)
        con.commit()


# Map local references to the database (handles if they exist already or not)
def get_works_cited_map(gw: Greenworld, con, data):
    works_cited_map = {}
    gw.log("Writing works cited...")
    last_id = get_last_id(con, orm.works_cited_table)
    for row in data["works_cited"] if "works_cited" in data else []:
        values = copy.deepcopy(row)
        works_cited_result = select_by(
            con, orm.works_cited_table, "citation", values["citation"]
        )
        if works_cited_result:
            works_cited_map[row["id"]] = works_cited_result["id"]
        else:
            values["id"] = last_id + 1
            works_cited_map[row["id"]] = values["id"]
            gw.log(f"INSERT {values}")
            con.execute(orm.works_cited_table.insert().values(**values))
            last_id += 1
    gw.log("")
    return works_cited_map


# Write ecological data with a many-to-many relationship to the database
def process_ecological_fields(gw: Greenworld, con, works_cited_map, plant_id, data):
    taxon = Taxon()
    for row in data:
        # Retrieve (and/or create) plant or non-plant species
        is_plant = True
        values = copy.deepcopy(row)
        values["species"] = taxon.parse(values["species"]).format()
        result = select_by(con, orm.plants_table, "species", values["species"])
        if not result:
            is_plant = False
            result = select_by(con, orm.other_species_table, "species", values["species"])
        if not result:
            species = values["species"]
            raise ValueError(f"Unknown interactive species '{species}'")
        if values["citation"] not in works_cited_map:
            citation_id = values["citation"]
            raise ValueError(f"Unknown citation with ID '{citation_id}'")
        interaction = {
            "plant": plant_id,
            "relationship": parse_enum(values["relationship"]),
            "citation": works_cited_map[values["citation"]],
        }

        # Insert or update in database
        if is_plant:
            interaction["target"] = result["id"]
            # pylint: disable-next=assignment-from-no-return
            and_clause = sqlalchemy.and_(
                orm.ecology_plant_table.c["plant"] == plant_id,
                orm.ecology_plant_table.c["target"] == result["id"],
            )
            existing = con.execute(
                orm.ecology_plant_table.select().where(and_clause)
            ).fetchone()
            if existing:
                gw.log(f"UPDATE {interaction}")
                con.execute(
                    orm.ecology_plant_table.update()
                    .where(and_clause)
                    .values(**interaction)
                )
            else:
                gw.log(f"INSERT {interaction}")
                con.execute(orm.ecology_plant_table.insert().values(**interaction))
        else:
            interaction["non_plant"] = result["id"]
            # pylint: disable-next=assignment-from-no-return
            and_clause = sqlalchemy.and_(
                orm.ecology_other_table.c["plant"] == plant_id,
                orm.ecology_other_table.c["non_plant"] == result["id"],
            )
            existing = con.execute(
                orm.ecology_other_table.select().where(and_clause)
            ).fetchone()
            if existing:
                gw.log(f"UPDATE {interaction}")
                con.execute(
                    orm.ecology_other_table.update()
                    .where(and_clause)
                    .values(**interaction)
                )
            else:
                gw.log(f"INSERT {interaction}")
                con.execute(orm.ecology_other_table.insert().values(**interaction))


def main(gw: Greenworld, args):
    db = orm.init_db()
    for a, _ in enumerate(args):
        if args[a] == "--help":
            print_help()
            break

        # Run the enter logic
        gw.log("")
        gw.log(f"Writing data from {args[a]}...")
        with open(args[a], "r", encoding="utf-8") as file:
            data = json.load(file)
            enter_data(gw, db, data)


if __name__ == "__main__":
    main(Greenworld(), sys.argv[1:])
