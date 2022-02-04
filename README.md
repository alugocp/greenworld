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

**Note:** This project targets Python 3.8

## Algorithm design
- Companionship groups are a selection of species that fill the niches within a companionship model (such as the forest garden model).
- We look at every combination of plants between different niches (smallest groups up to largest groups) and generate the compatibility report for each one. Larger groups can pull from a subgroup for some of its pairwise compatibility data.
- Pairwise compatibility is determined by nutrient uptake (per plant organ), synthesis, pest control, and preferred environment (soil pH and sunlight, maybe more factors one day). It is a list of factors that are labeled as beneficial, detrimental or neutral.
- Group compatibility is also determined by model-specific factors (the combination of certain niches, etc) that need to be recalculated per group.
- Each group is then assigned a recommended environment. This consists of a pH range, amount of sunlight, higher density of certain nutrients (for groups where the overall uptake exceeds average levels in some soil standard)

## Warehouse/UI design
The project uses a MongoDB database that gets populated by the core algorithm (written in Python).
Users can then query the database through a view that makes everything pretty.
There can be multiple interface tools that query the database, such as a command line tool or web GUI.