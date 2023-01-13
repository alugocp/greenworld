# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
The purpose of this project is to identify potential companion plant groups (a.k.a. `guilds`).

**Note:** This project targets `Python 3.8`

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by morphology, nutrients, non-plant relationships, allelopathy, and preferred environment.
A compatibility report consists of a set of suggested ranges to keep between two planted species.

## Commands
Use the following commands to help you while writing code for this project:

```bash
# Installs all Python dependencies
python3 -m pip install -r requirements.txt

# Runs the Python linter
python3 -m pylint greenworld
```

Then you can use the following commands while interacting with the database:

- `./run reset` hard resets the development database
- `./run report` generates companionship reports for newly added plant species
- `./run invalidate` invalidates the reports table so the next report command will iterate through every plant pair
- `./run query` prints a list of reports logged in the database
