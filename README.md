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
python3 -m pylint $(git ls-files "*.py")

# Performs unit tests
python3 run.py test
```

Then you can use the following commands while interacting with the database:

- `python3 run.py reset` hard resets the development database
- `python3 run.py report` generates companionship reports for newly added plant species
- `python3 run.py invalidate` invalidates the reports table so the next report command will iterate through every plant pair
- `python3 run.py query` prints a list of reports logged in the database

This command can be used to enter data into the database:

```bash
python3 enter.py [file [...]]
```

`file` arguments will point to files that adhere to one of the following structures.
Note that `scalar` refers to a string matching the pattern `[0-9](\.[0-9]+)? [a-z]+` such that it represents a measurement of some specific unit.

```js
// JSON files
{
  "plants": [
    {
      "id": number,
      "name": string,
      "species": string,
      "growth_habit": GrowthHabit enum value,
      "height": [scalar, scalar],
      "spread": [scalar, scalar],
      "root_spread": [scalar, scalar],
      "root_depth": [scalar, scalar],
      "nitrogen": Nitrogen enum value,
      "temperature": [scalar, scalar],
      "sun": Sun enum value,
      "soil": Soil enum value,
      "pH": [float, float],
      "drainage": Drainage enum value,
      "citations": {
          works_cited.id: [string, ...],
          ...
      }
    },
    ...
  ],
  "works_cited": [
    {
      "id": number,
      "citation": string
    },
    ...
  ]
}
```