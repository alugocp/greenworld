from greenworld.algorithm.canonical import CanonicalSuggestions as C
from greenworld.algorithm.algorithm import Algorithm
from greenworld.math.comparisons import overlaps
from greenworld.model.types import SuggestionSet
from greenworld.model.species import Species
algorithm = Algorithm()

# Returns the minimum distance to place two plants apart from one another
def minimum(s1: Species, s2: Species):
    return s1.roots[1] + s2.roots[1]

# Returns the maximum distance to place two plants apart from one another
def maximum(s1: Species, s2: Species):
    return minimum(s1, s2) + 10.0

# Pests, pollinators and diseases
@algorithm.register('Insect relationship factors')
def insect_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    # repels_pests (base on flavonoid synthesis)
    # sacrificial_crop (base on flavonoid synthesis)
    # attracts_friends (base on flavonoid synthesis)
    if s1.latin.split(' ')[0] == s2.latin.split(' ')[0]:
        # Go by taxonomic family for now
        s.append(C.similar_diseases(1.5, maximum(s1, s2)))
        # Go by flavonoid synthesis
        s.append(C.same_pests(5.0, maximum(s1, s2)))

# Allelopathy
@algorithm.register('Allelopathy and allelochemical factors')
def allelopathy_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    # bad_allelopathy (figure this section out later)
    # good_allelopathy (figure this section out later)
    pass

# Growth habit
@algorithm.register('Growth habit factors')
def growth_habit_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    # provides_shade (base on sunlight requirements and height difference)
    # vine_competition (base on vine size and lifecycle data)
    # sunlight_competition (base on sunlight requirements and height difference)
    # overgrowth_competition (base on time to seed and lifecycle data)
    # supress_weeds (base on growth habit for ground cover)
    if s1.duration.value < s2.duration.value and s1.roots[1] > s2.roots[1]:
        s.append(C.root_disruption(s1.roots[1] + s2.roots[1], maximum(s1, s2)))
    if s2.duration.value < s1.duration.value and s2.roots[1] > s1.roots[1]:
        s.append(C.root_disruption(s1.roots[1] + s2.roots[1], maximum(s1, s2)))
    if s1.roots[1] >= 0.5 and s1.drainage.value < s2.drainage.value:
        s.append(C.soil_loosener(1.0, 1.0))
    if s2.roots[1] >= 0.5 and s2.drainage.value < s1.drainage.value:
        s.append(C.soil_loosener(1.0, 1.0))

# Growth environment
@algorithm.register('Growth environment factors')
def environment_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    if not overlaps(s1.pH, s2.pH):
        s.append(C.ph_mismatch(minimum(s1, s2) + 1.0, maximum(s1, s2)))
    if s1.drainage != s2.drainage:
        s.append(C.drainage_mismatch(minimum(s1, s2) + 1.0, maximum(s1, s2)))
    if s1.water != s2.water:
        s.append(C.water_mismatch(minimum(s1, s2) + 1.0, maximum(s1, s2)))

# Nutrients
@algorithm.register('Nutrient use factors')
def nutrient_factors(s: SuggestionSet, s1: Species, s2: Species) -> None:
    # nitrogen_fixer (base on presence of luteolin and chrysin synthesis)
    # resource_competition (base on heavy feeder data)
    pass
