"""
This script validates that the Greenworld algorithm is indeed accurate
"""
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
    pair = [s1, s2]
    pair.sort()
    return " x ".join(pair)

# Expected companion results
BAD = {}
GOOD = {}
with open("scripts/validation.json", "r") as file:
    validation_data = json.loads(file.read())
for expectation in validation_data["expected"]:
    GOOD[expectation["host"]] = expectation["good"]
    BAD[expectation["host"]] = expectation["bad"]

# Generate report data
gw = Greenworld()
reset.main(gw, seed_data=False)
enter.main(gw, validation_data["sources"])
report.main(gw)

# Double check the companion data species names and duplicate pairs
db = init_db()
with db.connect() as con:
    db_species = con.execute(sqlalchemy.select(plants_table.c.species)).fetchall()
processed_pairs = []
species_names = list(map(lambda x: x["host"], validation_data["expected"]))
for expectation in validation_data["expected"]:
    for s in expectation["good"] + expectation["bad"]:
        pair = get_pair(expectation["host"], s)
        if not s in species_names:
            print(f"Unknown secondary species '{s}'")
            sys.exit(1)
        if pair in processed_pairs:
            print(f"Duplicate pair {pair}")
            sys.exit(1)
        processed_pairs.append(pair)
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
    if (s1 in GOOD and s2 in GOOD[s1]) or (s2 in GOOD and s1 in GOOD[s2]):
        good_dist.append(r["score"])
        good_reports.append(r)
    elif (s1 in BAD and s2 in BAD[s1]) or (s2 in BAD and s1 in BAD[s2]):
        bad_dist.append(r["score"])
        bad_reports.append(r)
    elif s1 in species_names and s2 in species_names:
        neutral_dist.append(r["score"])
        neutral_reports.append(r)

# Write report files
with open("scripts/garden-neutral-reports.txt", "w", encoding="utf-8") as file:
    file.write(json.dumps(neutral_reports, indent=4))
with open("scripts/garden-good-reports.txt", "w", encoding="utf-8") as file:
    file.write(json.dumps(good_reports, indent=4))
with open("scripts/garden-bad-reports.txt", "w", encoding="utf-8") as file:
    file.write(json.dumps(bad_reports, indent=4))


def percent_good(dist):
    """
    Percentage of "good" identified companions within a distribution
    """
    percent = len(list(filter(lambda x: x > 0, dist))) / len(dist)
    return round(percent * 10000) / 100


# Statistical comparison between distributions (Wilcoxon rank-sum tests)
# pylint: disable=consider-using-f-string
sys.stdout.write("\u001b[1mp-values\u001b[0m\n")
sys.stdout.write(
    "Good companions vs neutral: \u001b[31m%s\u001b[0m\n"
    % (stats.ranksums(good_dist, neutral_dist, alternative="greater").pvalue)
)
sys.stdout.write(
    "Bad companions vs neutral: \u001b[31m%s\u001b[0m\n"
    % (stats.ranksums(bad_dist, neutral_dist, alternative="less").pvalue)
)
sys.stdout.write(
    "Bad companions vs good: \u001b[31m%s\u001b[0m\n"
    % (stats.ranksums(bad_dist, good_dist, alternative="less").pvalue)
)
sys.stdout.write(
    "Good companions percentage of good companions: \u001b[31m%s\u001b[0m%%\n"
    % (percent_good(good_dist))
)
sys.stdout.write(
    "Good companions percentage of neutral companions: \u001b[31m%s\u001b[0m%%\n"
    % (percent_good(neutral_dist))
)
sys.stdout.write(
    "Good companions percentage of bad companions: \u001b[31m%s\u001b[0m%%\n"
    % (percent_good(bad_dist))
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
plt.savefig("scripts/garden.png")
