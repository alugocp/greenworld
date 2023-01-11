# This module contains the core logic for the Greenworld algorithm.
from defs import (
    GrowthHabit,
    Sun
)

# This variable is global for easy module-wide access
report = None

# This function creates and returns a new compatibility report
def guild_report(plant1, plant2):
    global report
    report = []
    can_vine_climb(plant1, plant2)
    return report

# Repeats the decorated function with the plants reversed
def mirrored(func):
    def wrapper(plant1, plant2):
        pair = func(plant1, plant2)
        if pair:
            report.append(pair)
        else:
            pair = func(plant2, plant1)
            if pair:
                report.append(pair)
    return wrapper

@mirrored
def can_vine_climb(plant1, plant2):
    if plant1.sun == Sun.FULL_SUN and plant1.growth_habit == GrowthHabit.VINE and plant1.fruit_weight < 0.1 and plant2.sun == Sun.FULL_SUN and plant2.growth_habit in [GrowthHabit.GRAMINOID, GrowthHabit.FORB]:
        return f'{plant1.name} can climb up {plant2.name} for direct sunlight'