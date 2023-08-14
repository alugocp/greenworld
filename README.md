# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
The purpose of this project is to identify potential companion plant groups (a.k.a. `guilds`).

**Note:** This project targets `Python 3.8`

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by morphology, nutrients, non-plant relationships, allelopathy, and preferred environment.
A compatibility report consists of a set of suggested ranges to keep between two planted species.

## Setup
This project uses a Postgres database hosted in Docker.
You must do the following in order to set it up:
```bash
# Record a database password
echo "PASSWORD=<SOME PASSWORD HERE>" > .env

# Run this if you've made recent Dockerfile changes
docker-compose build --no-cache

# Spin up the database and server
docker-compose up -d

# Stop the database and server
docker-compose down -v

# Access the database from the command line
psql -h localhost -p 5432 -U postgres -d greenworld
```

You can also use SQLite3 instead:
```bash
echo "DRIVER=sqlite" > .env
```

## Commands
Use the following commands to help you while writing code for this project:

```bash
# Installs all Python dependencies
make install

# Runs the linters
make lint

# Performs unit tests
make test

# Builds the frontend app code
make ui

# Starts the web server
make serve
```

Then you can use the following commands while interacting with the database:

- `make download` downloads all external data used by the database reset script
- `make reset` resets and reseeds the development database
- `make report` generates companionship reports for newly added plant species
- `make invalidate` invalidates the reports table so the next report command will iterate through every plant pair
- `make query` prints a list of reports logged in the database

### Data entry
This command can be used to enter data into the database:

```bash
make enter FILES=file,...
```

`file` arguments will point to files that adhere to a specific schema.
This schema can be found in the file [greenworld/schema.py](./greenworld/schema.py).
Example files can be found in the [seed-data](./seed-data) folder.

### Validation
These commands generate statistical values that validate the algorithm's accuracy:

- `make validate/sisters` generates error values for various traditional three sisters configurations
- `make validate/juglone` calculates error for walnut allelopathic range suggestion
- `make validate/garden` compares distributions for expected good, bad and neutral companions
