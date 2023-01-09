# Greenworld Algorithm
This is LugoCorp's companion planting data warehouse research project.
The purpose of this project is to identify potential companion plant groups (a.k.a. `guilds`).

**Note:** This project targets Python 3.8

## Algorithm design
The core algorithm looks at every combination of plants and generates a compatibility report for each one.
Pairwise compatibility is determined by growth habit, resource demand, non-plant relationships, allelopathy, and preferred environment.
A compatibility report consists of a set of suggested ranges to keep between two planted species.

## Commands
- `python -m pip install -r requirements.txt` installs all Python dependencies

## Todo

### Redesign
