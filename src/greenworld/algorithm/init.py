from typing import List
from greenworld.algorithm.algorithm import Algorithm
from greenworld.math.comparisons import overlaps
from greenworld.model.species import Species
from greenworld.model.factor import Factor
algorithm = Algorithm()

# Pests, pollinators and diseases
@algorithm.register('Insect relationship factors')
def insect_factors(factors: List[Factor], s1: Species, s2: Species) -> None:
    if s1.latin.split(' ')[0] == s2.latin.split(' ')[0]:
        factors.append(Factor(Factor.BAD,
            f'{s1} and {s2} may share diseases that affect their genus'
        ))

# Allelopathy
@algorithm.register('Allelopathy and allelochemical factors')
def allelopathy_factors(factors: List[Factor], s1: Species, s2: Species) -> None:
    pass

# Growth habit
@algorithm.register('Growth habit factors')
def growth_habit_factors(factors: List[Factor], s1: Species, s2: Species) -> None:
    if s1.duration.value < s2.duration.value and s1.roots[1] > s2.roots[1]:
        factors.append(Factor(Factor.BAD,
            f'{s1} has longer roots than {s2} and will be harvested earlier, possibly disrupting other roots'
        ))
    if s2.duration.value < s1.duration.value and s2.roots[1] > s1.roots[1]:
        factors.append(Factor(Factor.BAD,
            f'{s2} has longer roots than {s1} and will be harvested earlier, possibly disrupting other roots'
        ))
    if s1.roots[1] >= 0.5 and s1.drainage.value < s2.drainage.value:
        factors.append(Factor(Factor.GOOD,
            f'{s1} can loosen the soil for future {s2} crops'
        ))
    if s2.roots[1] >= 0.5 and s2.drainage.value < s1.drainage.value:
        factors.append(Factor(Factor.GOOD,
            f'{s2} can loosen the soil for future {s1} crops'
        ))

# Growth environment
@algorithm.register('Growth environment factors')
def environment_factors(factors: List[Factor], s1: Species, s2: Species) -> None:
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

# Nutrients
@algorithm.register('Nutrient use factors')
def nutrient_factors(factors: List[Factor], s1: Species, s2: Species) -> None:
    pass

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
