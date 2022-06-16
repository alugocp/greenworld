from greenworld.math.comparisons import overlaps
from greenworld.algorithm.algorithm import Algorithm
from greenworld.model.suggestion import SuggestionSet
from greenworld.model.types import SuggestionType
from greenworld.model.species import Species
algorithm = Algorithm()

# Pests, pollinators and diseases
@algorithm.register('Insect relationship factors')
def insect_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    if s1.latin.split(' ')[0] == s2.latin.split(' ')[0]:
        s.add('disease', (1.5, 1.5))

# Allelopathy
@algorithm.register('Allelopathy and allelochemical factors')
def allelopathy_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    pass

# Growth habit
@algorithm.register('Growth habit factors')
def growth_habit_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    if s1.duration.value < s2.duration.value and s1.roots[1] > s2.roots[1]:
        s.add('root disruption', (s1.roots[1] + s2.roots[1], s1.roots[1] + s2.roots[1]))
    if s2.duration.value < s1.duration.value and s2.roots[1] > s1.roots[1]:
        s.add('root disruption', (s1.roots[1] + s2.roots[1], s1.roots[1] + s2.roots[1]))
    if s1.roots[1] >= 0.5 and s1.drainage.value < s2.drainage.value:
        s.add('soil loosener', (1.0, 1.0), SuggestionType.TEMPORAL)
    if s2.roots[1] >= 0.5 and s2.drainage.value < s1.drainage.value:
        s.add('soil loosener', (1.0, 1.0), SuggestionType.TEMPORAL)

# Growth environment
@algorithm.register('Growth environment factors')
def environment_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    if not overlaps(s1.pH, s2.pH):
        s.add('pH mismatch', (1.0, 1.0))
    if s1.drainage != s2.drainage:
        s.add('drainage mismatch', (1.0, 1.0))
    if s1.water != s2.water:
        s.add('water mismatch', (1.0, 1.0))

# Nutrients
@algorithm.register('Nutrient use factors')
def nutrient_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
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
