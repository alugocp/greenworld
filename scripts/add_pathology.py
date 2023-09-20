import urllib.request
import json
import ssl
import sys
import re

# Extract the pathogen species list for a given species
def get_pathogen_species(species):
    print(f'• Retrieving pathogens for {species}...')
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    species = species.replace(' ', '+')
    url = f'http://www.phi-base.org/searchFacet.htm?queryTerm={species}'
    with urllib.request.urlopen(url, context = context) as data:
        content = data.read().decode('utf-8')
        results = re.findall(r'<input  name=\'Pathogen_species\' type=\'checkbox\' value=\'([A-Za-z ]+)\'', content)
        return list(map(lambda x: x.lower(), results))

# Process a single seed data file
def process_data_file(filepath):
    print(f'Reading {filepath}...')
    with open(filepath, 'r') as file:
        data = json.loads(file.read())

    # Set up the citations
    works_cited = data['works_cited'] if 'works_cited' in data else []
    citation_id = max(list(map(lambda x: x['id'], works_cited))) + 1
    works_cited.append({ 'id': citation_id, 'citation': 'http://www.phi-base.org/searchFacet.htm?queryTerm=' })
    data['works_cited'] = works_cited

    # Grab pathogens for each plant species
    other_species = data['others'] if 'others' in data else []
    for plant in (data['plants'] if 'plants' in data else []):
        pathogens = get_pathogen_species(plant['species'])

        # Add the pathogen if they're not already listed for this plant species
        ecology = plant['ecology'] if 'ecology' in data else []
        for pathogen in pathogens:
            if not any(pathogen == partner['species'] for partner in ecology):
                ecology.append({ 'species': pathogen, 'relationship': 'Ecology.PATHOGEN', 'citation': citation_id })
            if not any(pathogen == species['species'] for species in other_species):
                other_species.append({ 'species': pathogen, 'name': 'unknown' })
        if len(ecology) > 0:
            plant['ecology'] = ecology
    data['others'] = other_species

    # Write changed data back to the original file
    with open(filepath, 'w') as file:
        file.write(json.dumps(data, indent = 4))

# Iterate through the list of requested files' plant species,
# request data from PHI Base, and write back to those files
if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        process_data_file(filepath)
