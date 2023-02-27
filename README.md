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
make install

# Runs the Python linter
make lint

# Performs unit tests
make test

# Starts the web server
make serve
```

Then you can use the following commands while interacting with the database:

- `make reset` hard resets the development database
- `make report` generates companionship reports for newly added plant species
- `make invalidate` invalidates the reports table so the next report command will iterate through every plant pair
- `make query` prints a list of reports logged in the database

This command can be used to enter data into the database:

```bash
make enter FILES=file,...
```

`file` arguments will point to files that adhere to one of the following structures.
Note that `scalar` refers to a string matching the pattern `[0-9](\.[0-9]+)? [a-z]+` such that it represents a measurement of some specific unit.

```js
{
  "plants": [
    {
      "id": integer, // required
      "name": string, // required
      "species": string, // required
      "family": string, // required
      "growth_habit": GrowthHabit enum value,
      "fruit_weight": [scalar, scalar],
      "height": [scalar, scalar],
      "spread": [scalar, scalar],
      "length": [scalar, scalar],
      "root_spread": [scalar, scalar],
      "root_depth": [scalar, scalar],
      "nitrogen": Nitrogen enum value,
      "temperature": [scalar, scalar],
      "sun": Sun enum value,
      "soil": Soil enum value,
      "pH": [float, float],
      "drainage": Drainage enum value,
      "citations": { // required
          works_cited.id as a string: [plant field, ...],
          ...
      },
      "ecology": [
          {
              "species": string, // required
              "relationship": Ecology enum value, // required
              "citation": works_cited.id // required
          },
          ...
      ]
    },
    ...
  ],
  "others": [
    {
        "species": "string", // required
        "name": "string", // required
        "family": "string"
    },
    ...
  ]
  "works_cited": [
    {
      "id": integer, // required
      "citation": string // required
    },
    ...
  ]
}
```