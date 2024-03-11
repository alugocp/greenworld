import sys
import csv
import json
import sqlalchemy
from greenworld import Greenworld
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.scripts import report
from greenworld.orm import plants_table
from greenworld.orm import reports_table
from greenworld.orm import init_db


def main():
    """
    Main logic for this validation script
    """

    # Initialize database state
    gw = Greenworld()
    reset.main(gw, False)
    enter.main(gw, ["seed-data/lit-review.json"])
    report.main(gw)

    # Retrieve all used citations (used to auto-filter the companion data)
    referenced = set()
    with open("seed-data/lit-review.json", "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    for plant in data["plants"]:
        for x in plant["ecology"] if "ecology" in plant else []:
            referenced.add(x["citation"])
    for other in data["others"]:
        for x in other["predators"] if "predators" in other else []:
            referenced.add(x["citation"])

    # Filter expected companionship data by referenced citations
    companions = []
    with open(
        "validation/Literature Review - Plant Pairs - Pairs.csv", "r", encoding="utf-8"
    ) as file:
        data = csv.reader(file)
        for row in data:
            if any(x.isnumeric() and int(x) in referenced for x in row[3].split(", ")):
                companions.append(row[0:3])

    # Query Greenworld for the calculated compatibility scores
    p1 = plants_table.alias("p1")
    p2 = plants_table.alias("p2")
    stmt = (
        sqlalchemy.select(p1.c["species"], p2.c["species"], reports_table.c["score"])
        .join(p1, p1.c["id"] == reports_table.c["plant1"])
        .join(p2, p2.c["id"] == reports_table.c["plant2"])
    )

    # Create 3 distributions of scores based on their expected companionship
    NEUTRAL_SCORES = []
    GOOD_SCORES = []
    BAD_SCORES = []
    SCORES_LOG = []
    db = init_db()
    with db.connect() as con:
        for result in con.execute(stmt):
            p1, p2, score = result
            catch = next(filter(lambda x: p1 in x and p2 in x, companions), None)
            if catch:
                {"NEUTRAL": NEUTRAL_SCORES, "GOOD": GOOD_SCORES, "BAD": BAD_SCORES}[
                    catch[2]
                ].append([p1, p2, score])
                SCORES_LOG.append([p1, p2, score])

    if len(SCORES_LOG) < len(companions):
        diff = len(companions) - len(SCORES_LOG)
        print(
            f"Missing {diff} scores from database! Perhaps the species names weren't parsed correctly?"
        )
        sys.exit(1)

    print([(float(x[2]) if x[2] else 0) for x in NEUTRAL_SCORES])
    print([(float(x[2]) if x[2] else 0) for x in GOOD_SCORES])
    print([(float(x[2]) if x[2] else 0) for x in BAD_SCORES])


if __name__ == "__main__":
    main()
