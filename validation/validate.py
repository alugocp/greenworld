"""
This script validates that the Greenworld algorithm is indeed accurate
"""
import os
import re
import sys
import json
import sqlalchemy
import matplotlib.pyplot as plt
from scipy import stats
from greenworld.scripts import report
from greenworld.scripts import reset
from greenworld.scripts import enter
from greenworld import Greenworld
from greenworld.orm import reports_table
from greenworld.orm import plants_table
from greenworld.orm import init_db

# Potential sources of error:
#  - Certain good or bad pairs are missing from this data set
#  - Plant data is missing or inaccurate
#  - The algorithm needs tweaks


def get_pair(s1, s2):
    """
    Deterministic identifier for a pair of plant species
    """
    pair = [s1, s2]
    pair.sort()
    return " x ".join(pair)


def validate(filename):
    """
    Runs the Greenworld algorithm on a set of plant data, then
    performs rank-sum tests on distributions of compatibility scores
    against a set of expected good and bad companion pairs
    """
    sys.stdout.write(f"Processing {filename}...\n")

    # Read the validation test data file
    with open(f"validation/data/{filename}.json", "r", encoding = "utf-8") as file:
        validation_data = json.loads(file.read())

    # Check for unrepresented species or duplicate pairs
    processed_pairs = []
    duplicate_pairs = []
    species_names = list(map(lambda x: x["host"], validation_data["expected"]))
    for expectation in validation_data["expected"]:
        for s in expectation["good"] + expectation["bad"]:
            pair = get_pair(expectation["host"], s)
            if not s in species_names:
                print(f"Unknown secondary species '{s}'")
                sys.exit(1)
            if pair in processed_pairs:
                duplicate_pairs.append(pair)
            processed_pairs.append(pair)

    # Exit if there are any duplicate pairs
    if len(duplicate_pairs) > 0:
        for pair in duplicate_pairs:
            print(f"Duplicate pair {pair}")
        sys.exit(1)

    # Cache the expected pair qualities
    PAIRS = {}
    for expectation in validation_data["expected"]:
        for s in expectation["good"]:
            PAIRS[get_pair(expectation["host"], s)] = True
        for s in expectation["bad"]:
            PAIRS[get_pair(expectation["host"], s)] = False

    # Generate report data
    gw = Greenworld()
    reset.main(gw, seed_data=False)
    enter.main(gw, validation_data["sources"])
    report.main(gw)

    # Check that every referenced species is in the database
    db = init_db()
    with db.connect() as con:
        db_species = con.execute(sqlalchemy.select(plants_table.c.species)).fetchall()
    for name in species_names:
        if (name,) not in db_species:
            print(f"Unknown species '{name}'")
            sys.exit(1)

    # Retrieve compatibility scores
    plant_1_table = sqlalchemy.alias(plants_table)
    plant_2_table = sqlalchemy.alias(plants_table)
    stmt = (
        sqlalchemy.select(
            reports_table.c.score,
            reports_table.c.report,
            plant_1_table.c.species.label("species1"),
            plant_2_table.c.species.label("species2"),
        )
        .join(plant_1_table, reports_table.c.plant1 == plant_1_table.c.id)
        .join(plant_2_table, reports_table.c.plant2 == plant_2_table.c.id)
        .where(reports_table.c.score is not None)
    )

    with db.connect() as con:
        results = list(map(dict, con.execute(stmt).mappings().fetchall()))

    # Create the distributions and reports
    neutral_reports = []
    neutral_dist = []
    good_reports = []
    good_dist = []
    bad_reports = []
    bad_dist = []
    for r in results:
        r["score"] = 0.0 if r["score"] is None else float(r["score"])
        s1 = r["species1"]
        s2 = r["species2"]
        pair = get_pair(s1, s2)
        quality = PAIRS[pair] if pair in PAIRS else None
        if quality == True:
            good_dist.append(r["score"])
            good_reports.append(r)
        elif quality == False:
            bad_dist.append(r["score"])
            bad_reports.append(r)
        elif s1 in species_names and s2 in species_names:
            neutral_dist.append(r["score"])
            neutral_reports.append(r)

    # Write report files
    with open(f"validation/{filename}-neutral.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(neutral_reports, indent=4))
    with open(f"validation/{filename}-good.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(good_reports, indent=4))
    with open(f"validation/{filename}-bad.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(bad_reports, indent=4))

    def percent_quality(dist, good=True):
        """
        Percentage of "good" identified companions within a distribution
        """
        if len(dist) == 0:
            return 0
        l = (lambda x: x > 0) if good else (lambda x: x < 0)
        percent = len(list(filter(l, dist))) / len(dist)
        return round(percent * 10000) / 100

    # Statistical comparison between distributions (Wilcoxon rank-sum tests)
    # pylint: disable=consider-using-f-string
    sys.stdout.write("\u001b[1mp-values\u001b[0m\n")
    sys.stdout.write(
        "Good companions vs neutral: \u001b[31m%s\u001b[0m\n"
        % (stats.ranksums(good_dist, neutral_dist, alternative="greater").pvalue)
    )
    if len(bad_dist) > 0:
        sys.stdout.write(
            "Bad companions vs neutral: \u001b[31m%s\u001b[0m\n"
            % (stats.ranksums(bad_dist, neutral_dist, alternative="less").pvalue)
        )
        sys.stdout.write(
            "Bad companions vs good: \u001b[31m%s\u001b[0m\n"
            % (stats.ranksums(bad_dist, good_dist, alternative="less").pvalue)
        )
    sys.stdout.write("---\n")
    sys.stdout.write(
        "Good companions percentage of good companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(good_dist))
    )
    sys.stdout.write(
        "Bad companions percentage of good companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(good_dist, False))
    )
    sys.stdout.write("---\n")
    sys.stdout.write(
        "Good companions percentage of neutral companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(neutral_dist))
    )
    sys.stdout.write(
        "Bad companions percentage of neutral companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(neutral_dist, False))
    )
    sys.stdout.write("---\n")
    sys.stdout.write(
        "Good companions percentage of bad companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(bad_dist))
    )
    sys.stdout.write(
        "Bad companions percentage of bad companions: \u001b[31m%s\u001b[0m%%\n"
        % (percent_quality(bad_dist, False))
    )
    # pylint: enable=consider-using-f-string

    # Plot distributions and save to image
    common = {"histtype": "step", "bins": 100}
    plt.set_loglevel(level="warning")
    plt.title("Compatibility Scores for Companions of Expected Quality")
    plt.xlabel("Compatibility score")
    plt.ylabel("Frequency")
    plt.hist(good_dist, **common, color="green", label="Expected good pairs")
    plt.hist(neutral_dist, **common, color="blue", label="Expected neutral pairs")
    plt.hist(bad_dist, **common, color="red", label="Expected bad pairs")
    plt.legend()
    plt.savefig(f"validation/{filename}.png")


def run_all_validation():
    """
    Runs the validation method for all data files
    """
    data_files = os.listdir("validation/data")
    for file in data_files:
        filename = re.match(r"^(\w+)\.json$", file).groups()[0]
        validate(filename)

if __name__ == "__main__":
    run_all_validation()
