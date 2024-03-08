import sys
import json
from greenworld.schema import json_schema
from greenworld.taxonomy import Taxon
# TODO add the following to this script:
# • Check for duplicate species in plants, others, or ecology entries
# • Check for citation IDs that don't exist
# • Check for duplicate citations and smush them together

# Validate that the seed data matches our schema
def validate_schema(data):
    if json_schema.validate(data) != data:
        print("File does not match the schema")
        sys.exit(1)

# Pass all referenced species names through the taxonomic formatter
def taxonomize_species(data):
    taxon = Taxon()

    # Taxonomize plant species and their ecological interactions
    for plant in (data["plant"] if "plant" in data else []):
        plant["species"] = taxon.parse(plant["species"]).format()
        for other in (plant["ecology"] if "ecology" in plant else []):
            other["species"] = taxon.parse(other["species"]).format()

    # Taxonomize nonplant species and their ecological interactions
    for nonplant in (data["others"] if "others" in data else []):
        nonplant["species"] = taxon.parse(nonplant["species"]).format()
        for other in (nonplant["ecology"] if "ecology" in nonplant else []):
            other["species"] = taxon.parse(other["species"]).format()

# Names species that are named ??? after their genus instead
def assign_missing_names_by_genus(data):
    taxon = Taxon()

    # Assign missing names for plant species
    for plant in (data["plant"] if "plant" in data else []):
        if plant["name"] == "???":
            plant["name"] = taxon.parse(plant["species"]).genus

    # Assign missing names for nonplant species
    for nonplant in (data["others"] if "others" in data else []):
        if nonplant["name"] == "???":
            nonplant["name"] = taxon.parse(nonplant["species"]).genus

def main(args):
    for filepath in args:
        # Read the requested seed data file
        print(f"Linting {filepath}...")
        in_file = open(filepath, "r", encoding = "utf-8")
        data = json.loads(in_file.read())

        # Perform linting procedures
        validate_schema(data)
        taxonomize_species(data)
        assign_missing_names_by_genus(data)

        # Write modified data back to the file
        out_file = open(filepath, "w", encoding = "utf-8")
        out_file.write(json.dumps(data, indent = 4))
        print(f"Linted {filepath}!")

if __name__ == "__main__":
    main(sys.argv[1:])
