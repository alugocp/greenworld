from typing import List
from greenworld.model.factor import Factor
from greenworld.model.species import Species
from greenworld.math.comparisons import overlaps

# This function calculates a compatibility report for the given pair of species.
def calculate_compatibility(s1: Species, s2: Species) -> List[Factor]:
    factors = []
    if not overlaps(s1.pH, s2.pH):
        factors.append(Factor(Factor.BAD,
            f'{s1} and {s2} require different soil pH levels'
        ))
    if s1.drainage != s2.drainage:
        factors.append(Factor(Factor.BAD,
            f'{s1} and {s2} require different soil drainage levels'
        ))
    if s1.water != s2.water:
        factors.append(Factor(Factor.NEUTRAL,
            f'{s1} and {s2} will need different levels of water'
        ))
    # Bad if soil pH levels don't overlap
    # Bad if species have the same diseases or pests
    # Good, plant far away if one plant attracts another one's pests
    # Good if one plant prohibits another plant's pests
    # Plant far enough away for similar root length plants to not compete
    # Plant far enough away for plants of differing height to not compete for sunlight
    # Good if a vining plant is grown up a stalky plant
    # Good if one plant synthesizes a nutrient required by another plant
    # Good if one plant attracts pollinators (and the other needs pollinators)
    # If same species and may cross pollinate, suggest either planting far away or get hybrid
    # Good if the shorter plant likes some shade (provided by taller plant)
    # Plant farther away if one plant needs more water than another
    # Plant shallow root plants away from root crops (so root harvest doesn't disrupt shallow roots)
    return factors
