import sys
import json
from typing import Set, List
from greenworld.schema import json_schema
from greenworld.taxonomy import Taxon
RESULT = 0

def log_error(msg: str):
    global RESULT
    print(f"• {msg}")
    RESULT = 1

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
        for other in (nonplant["predators"] if "predators" in nonplant else []):
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

# Identify strings that are repeated in a list of strings
def find_repeats(lst: List[str]) -> Set[str]:
    unique = set(lst)
    if len(unique) == len(lst):
        return []
    duplicates = set()
    for x in lst:
        if x in unique:
            unique.remove(x)
        else:
            duplicates.add(x)
    return duplicates

# Identify repeat species in lists throughout the data
def identify_repeat_species(data):
    # Look for duplicates in plants
    dups = find_repeats(list(map(lambda x: x["species"], data["plants"] if "plants" in data else [])))
    if len(dups) > 0:
        formatted = ", ".join(dups)
        log_error(f"Duplicate species found in plants: {formatted}")

    # Look for duplicates in others
    dups = find_repeats(list(map(lambda x: x["species"], data["others"] if "others" in data else [])))
    if len(dups) > 0:
        formatted = ", ".join(dups)
        log_error(f"Duplicate species found in others: {formatted}")

    # Look for duplicates in each plants' ecology field
    for species in (data["plants"] if "plants" in data else []):
        dups = find_repeats(list(map(lambda x: x["species"], species["ecology"] if "ecology" in species else [])))
        if len(dups) > 0:
            formatted = ", ".join(dups)
            name = species["species"]
            log_error(f"Duplicate ecological partners found for {name}: {formatted}")

    # Look for duplicates in each non-plants' predators field
    for species in (data["others"] if "others" in data else []):
        dups = find_repeats(list(map(lambda x: x["species"], species["predators"] if "predators" in species else [])))
        if len(dups) > 0:
            formatted = ", ".join(dups)
            name = species["species"]
            log_error(f"Duplicate predators found for {name}: {formatted}")

# Traverse through all citation data and check for duplicates or missing links
def audit_and_organize_citations(data):
    works_cited = data["works_cited"] if "works_cited" in data else []
    dups = find_repeats(list(map(lambda x: x["citation"], works_cited)))
    citation_map = {}

    # Populate the duplicate citation map
    for citation in dups:
        relevant = list(filter(lambda x: x["citation"] == citation, works_cited))
        new_id = relevant[0]["id"]
        for derived in relevant[1:]:
            past_id = derived["id"]
            citation_map[past_id] = new_id
            works_cited.remove(derived)
            print(f"• Duplicate work cited {past_id} will be changed to {new_id}")

    # Collect the remaining citation IDs for easy lookup
    citations = list(map(lambda x: x["id"], works_cited))

    # Audit the citations in the plant ecology field
    for species in (data["plants"] if "plants" in data else []):
        for interaction in (species["ecology"] if "ecology" in species else []):
            citation = interaction["citation"]
            if citation in citation_map:
                citation = citation_map[citation]
            elif citation not in citations:
                log_error(f"Unknown citation {citation}")

    # Audit the citations in the nonplant predators field
    for species in (data["others"] if "others" in data else []):
        for interaction in (species["predators"] if "predators" in species else []):
            citation = interaction["citation"]
            if citation in citation_map:
                citation = citation_map[citation]
            elif citation not in citations:
                log_error(f"Unknown citation {citation}")

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
        identify_repeat_species(data)
        audit_and_organize_citations(data)

        # Write modified data back to the file
        out_file = open(filepath, "w", encoding = "utf-8")
        out_file.write(json.dumps(data, indent = 4))
        print(f"Linted {filepath}!")

if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(RESULT)
