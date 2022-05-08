# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
This README contains all the information you'll need to initialize the warehouse and run the core algorithms.
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
Pairwise compatibility is determined by nutrient uptake (per plant organ), nutrient synthesis, pest control, and preferred environment (soil pH and sunlight, maybe more factors one day). It is a list of factors that are labeled as beneficial, detrimental or suggestions for planting these two species together.

## Warehouse/UI design
The project uses a MongoDB database that gets populated by the core algorithm (written in Python).
Users can then query the database through a view that makes everything pretty.
There can be multiple interface tools that query the database, such as a command line tool or web GUI.