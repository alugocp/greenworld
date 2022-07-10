# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
This `README` contains all the information you'll need to initialize the warehouse and run the core algorithms.
The purpose of this project is to identify potential companion farming groups and to query those groups by target environmental factors.

## Tasks
These commands will help you throughout development and deployment of this project.

- `python3 -m pip install -r requirements.txt` installs all project dependencies
- `python3 -m pylint src` lints the project code
- `./gw run` runs the core algorithm
- `./gw` views the project options
- `./tests` runs all the unit tests

**Note:** This project targets Python 3.8

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by growth habit, preferred environment, nutrient chemistry, insect relationships, and allelopathy.
It is a list of suggested spatial and temporal ranges for planting any two crops in relation to each other.

## Warehouse/UI design
The project uses a MongoDB database that gets populated by the core algorithm (written in Python).
Users can then query the database through a view that makes everything pretty.
There can be multiple interface tools that query the database, such as a command line tool or web GUI.

## Todo

### Getting Started
- [x] Set up algorithm basics
- [x] Write a printer that makes console output easy
- [x] Write the CLI to run the core algorithm
- [x] Create an iterator for every combination of species from different niches
- [x] Add custom types for readability (Species, Niche and Niches mainly)
- [x] Run pip for the first time to start using dependencies
- [x] Start linting the code
- [x] Add some tests for the combinations logic
- [x] Work out the species type (have it be more complex than just str)
- [x] Do dependency injection
- [x] Write argument parsing
- [x] Add help and version commands (with usage/credits displayed)

### Algorithm Development and Validation
- [x] Gather a group of species for validation tests
- [x] Write some basic companionship rules
- [x] Write a validation test based on expected companion groups and anti-companion groups
- [x] Find out where to get biochemical pathway data for crops (to see input/output nutrient forms) (perhaps nutrient uptake and nutrient level data)
- [ ] Tweak algorithm rules and add data as needed until tests look good
- [ ] Develop a concrete schema for species data

### Expanding on the Algorithm
- [ ] Connect the data to a database (write new implementations for data output)
- [ ] Implement queries by preferred crop(s)
- [ ] Investigate taxonomic granularity (maybe some data can be recorded at the genus or family level, for example)
- [ ] Optimize companion group analysis somehow
- [ ] Start expanding the plant data available to the algorithm
- [ ] Write an outline and rough draft of a paper

### Ready for Publication
- [ ] Implement queries by preferred soil/environment
- [ ] Look for a potential paper publisher
- [ ] Allow users to query the companion groups view through the CLI (using SQL?)
- [ ] Reorganize schema and CLI interface for deployment (if needed)
- [ ] Write second draft of paper with all recent changes in mind
- [ ] Write a YouTube video outline