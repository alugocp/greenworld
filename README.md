# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
The purpose of this project is to identify potential companion plant groups (a.k.a. `guilds`).

**Note:** This project targets `Python 3.8`

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by morphology, nutrients, non-plant relationships, allelopathy, and preferred environment.
A compatibility report consists of a set of suggested ranges to keep between two planted species.

## Commands
Use the following code to setup the project for the first time:

```bash
# Installs all Python dependencies
python3 -m pip install -r requirements.txt
```

Then you can use the following commands throughout development:

- `./run reset` hard resets the development database
- `./run report` generates companionship reports for newly added plant species
- `./run invalidate` invalidates the reports table so the next report command will iterate through every plant pair
