import sys
import csv
import json
import sqlalchemy
from scipy.stats import mannwhitneyu
from greenworld import Greenworld
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld.scripts import report
from greenworld.orm import plants_table
from greenworld.orm import reports_table
from greenworld.orm import init_db



def mann_whitney(label, d1, d2):
    """
    Performs a Mann-Whitney U test against two distributions and prints the outcome
    """
    p = mannwhitneyu(d1, d2, alternative = "greater").pvalue
    result = "\033[31mNULL ACCEPTED" if p > 0.05 else "\033[32mNULL REJECTED"
    sys.stdout.write(f"\033[1m{label}: {result}\033[0m\n")

def main():
    """
    Main logic for this validation script
    """

    # Initialize database state
    gw = Greenworld()
    if input("Reinitialize database? (y/N): ").lower() == "y":
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

    # Filter expected companionship data by referenced citations, and only
    # allow one expected companionship value per plant species pairing
    companions = []
    with open(
        "validation/Literature Review - Plant Pairs - Pairs.csv", "r", encoding="utf-8"
    ) as file:
        data = csv.reader(file)
        for row in data:
            if any(x.isnumeric() and int(x) in referenced for x in row[3].split(", ")) and not any((x[0] == row[0] and x[1] == row[1]) for x in companions):
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
    BASELINE = [0 for _ in range(10)]
    db = init_db()
    with db.connect() as con:
        for result in con.execute(stmt):
            p1, p2, score = result
            catch = next(filter(lambda x: (p1 == x[0] and p2 == x[1]) or (p2 == x[0] and p1 == x[1]), companions), None)
            if catch:
                SCORES_LOG.append([p1 if p1 < p2 else p2, p2 if p1 < p2 else p1, float(score or 0)])
                {"NEUTRAL": NEUTRAL_SCORES, "GOOD": GOOD_SCORES, "BAD": BAD_SCORES}[
                    catch[2]
                ].append(float(score or 0))

    companions.sort(key=lambda x: ", ".join(x[0:2]))
    SCORES_LOG.sort(key=lambda x: ", ".join(x[0:2]))
    if len(SCORES_LOG) < len(companions):
        diff = len(companions) - len(SCORES_LOG)
        print(
            f"Missing {diff} scores from database! Perhaps the species names weren't parsed correctly?"
        )

        print("Companions | SCORES_LOG")
        for i, x in enumerate(companions):
            y = SCORES_LOG[i] if i < len(SCORES_LOG) else None
            print(f"{x} | {y}")
        sys.exit(1)

    sys.stdout.write(f"\033[1mNeutral scores:\033[0m {NEUTRAL_SCORES}\n")
    sys.stdout.write(f"\033[1mGood scores:\033[0m {GOOD_SCORES}\n")
    sys.stdout.write(f"\033[1mBad scores:\033[0m {BAD_SCORES}\n")
    sys.stdout.write(f"\033[1mBaseline:\033[0m {BASELINE}\n")
    # Mann-Whitney U tests:
    # • Expect GOOD_SCORES to reject the null hypothesis against NEUTRAL_SCORES
    # • Expect NEUTRAL_SCORES to reject the null hypothesis against BAD_SCORES
    # • Expect GOOD_SCORES to reject the null hypothesis against BAD_SCORES
    # • Expect NEUTRAL_SCORES to accept the null hypothesis against [ 0 ]
    # • Expect GOOD_SCORES to reject the null hypothesis against [ 0 ]
    # • Expect BAD_SCORES to reject the null hypothesis against [ 0 ]
    mann_whitney("GOOD > NEUTRAL", GOOD_SCORES, NEUTRAL_SCORES)
    mann_whitney("NEUTRAL > BAD", NEUTRAL_SCORES, BAD_SCORES)
    mann_whitney("GOOD > BAD", GOOD_SCORES, BAD_SCORES)
    mann_whitney("GOOD > BASELINE", GOOD_SCORES, BASELINE)
    mann_whitney("NEUTRAL > BASELINE", NEUTRAL_SCORES, BASELINE)
    mann_whitney("BASELINE > BAD", BASELINE, BAD_SCORES)


if __name__ == "__main__":
    main()
