# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
The purpose of this project is to identify potential companion plant groups (a.k.a. `guilds`).

**Note:** This project targets `Python 3.11.8` via PyEnv

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by morphology, nutrients, non-plant relationships, allelopathy, and preferred environment.
A compatibility report consists of a set of suggested ranges to keep between two planted species.

## Setup
This Python project uses PyEnv for version control and has several dependencies.
Here is how you install them all:
```bash
# Install PyEnv
curl https://pyenv.run | bash

# You may need to run this line on Linux systems if _sqlite3 is missing
# (uninstall the project version of Python, then run this, then reinstall Python)
sudo apt install libsqlite3-dev

# Install the project's Python version
pyenv install 3.11.8

# Add the PyEnv hooks to your ~/.bashrc script if you'd like,
# just make sure that you're on the right version of Python

# Install all dependencies
python -m pip install -r requirements.txt
npm install
```

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

# Performs the statistical validation test
make validate

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

### Data entry
This command can be used to enter data into the database:

```bash
make enter FILES=file,...
```

`file` arguments will point to files that adhere to a specific schema.
This schema can be found in the file [greenworld/schema.py](./greenworld/schema.py).
Example files can be found in the [seed-data](./seed-data) folder.

### Data collection
This command can be used to automatically collect and insert relevant data into seed data files.

```bash
make collect FILES=file,...
```

`file` arguments follow the same guidelines as the `make enter` script, but this script can also input other formats (see `referenced-data/clements_1923.xls`).

### Data linting
This command can be used to lint seed data files.

```bash
make format FILES=file,...
```

`file` arguments follow the same guidelines as the `make enter` script.

### Project Navigation
- `frontend`: TypeScript code for the Greenworld browser-based UI
- `greenworld`: Greenworld code and maintenance scripts
- `journal`: Notes used to aid development
- `referenced-data`: Datasets used to feed `seed-data`
- `scripts`: Miscellaneous scripts that don't fit anywhere else
- `seed-data`: Data used to seed Greenworld instances
- `server`: Greenworld web server
