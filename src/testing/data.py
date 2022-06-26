# This file defines expected GreenWorld output for various selected companion plants.
# Every plant listed here should also be listed in src/testing/plants.txt.
# TODO remove src/tsting/(anti)*companions.txt when this file is fully implemented.
from greenworld.algorithm.canonical import CanonicalSuggestions as C

def generate_validation_data():
	return {
		'potato': {
			'garlic': [ C.repels_pests() ],
			'onion': [ C.repels_pests() ],
			'peas': [ C.nitrogen_fixer() ],
			'beans': [ C.nitrogen_fixer() ],
			'corn': [ C.provides_shade() ],
			'basil': [ C.repels_pests() ],
			'parsley': [ C.sacrificial_crop() ],
			'marigold': [ C.sacrificial_crop() ],
			'nasturtium': [ C.sacrificial_crop() ],
			'squash': [ C.resource_competition(), C.similar_diseases() ],
			'carrots': [ C.root_disruption() ],
			'sunflower': [ C.bad_allelopathy() ],
			'fennel': [ C.bad_allelopathy() ]
		},
		'tomato': {
			'basil': [ C.repels_pests() ],
			'beans': [  ], # Similar preferred environment, fill in more specifically later
			'carrots': [ C.soil_loosener() ],
			'chives': [ C.good_allelopathy() ],
			'garlic': [ C.repels_pests() ],
			'marigold': [ C.repels_pests() ],
			'mint': [ C.good_allelopathy() ],
			'nasturtium': [ C.sacrificial_crop() ],
			'onion': [ C.repels_pests() ],
			'parsley': [ C.good_allelopathy() ],
			'squash': [  ], # Unknown reasons, look into later
			'corn': [ C.same_pests() ],
			'peppers': [ C.same_pests() ],
			'potato': [ C.same_pests() ],
			'fennel': [ C.bad_allelopathy() ]
		},
		'onion': {
			'peppers': [ C.repels_pests() ],
			'carrots': [ C.repels_pests() ],
			'parsley': [ C.repels_pests() ],
			'beans': [ C.bad_allelopathy() ],
			'peas': [ C.bad_allelopathy() ],
			'garlic': [ C.same_pests() ],
			'chives': [ C.same_pests() ]
		},
		'corn': {
			'squash': [ C.supress_weeds() ],
			'beans': [ C.nitrogen_fixer() ],
			'watermelon': [ C.supress_weeds() ],
			'marigold': [ C.attracts_friends() ],
			'mint': [ C.repels_pests() ],
			'nasturtium': [ C.sacrificial_crop() ],
			'sunflower': [ C.attracts_friends() ],
			'fennel': [ C.bad_allelopathy() ]
		},
		'squash': {
			'nasturtium': [ C.attracts_friends(), C.sacrificial_crop() ],
			'beans': [ C.nitrogen_fixer(), C.repels_pests() ],
			'marigold': [ C.repels_pests() ],
			'peas': [ C.nitrogen_fixer() ],
			'mint': [ C.attracts_friends() ]
		},
		'beans': {
			'nasturtium': [ C.sacrificial_crop() ],
			'peas': [ C.nitrogen_fixer() ],
			'carrots': [ C.nitrogen_fixer(), C.repels_pests() ],
			'chives': [ C.bad_allelopathy() ],
			'garlic': [ C.bad_allelopathy() ],
			'peppers': [ C.vine_competition() ],
			'sunflower': [ C.bad_allelopathy() ]
		},
		'mint': {
			'beans': [ C.repels_pests() ],
			'carrots': [ C.repels_pests() ],
			'onion': [ C.repels_pests() ],
			'peas': [ C.repels_pests() ],
			'peppers': [ C.repels_pests() ]
		},
		'watermelon': {
			'onion': [ C.repels_pests() ],
			'garlic': [ C.repels_pests() ],
			'chives': [ C.repels_pests() ],
			'beans': [ C.nitrogen_fixer() ],
			'carrots': [ C.soil_loosener() ],
			'mint': [ C.repels_pests() ],
			'nasturtium': [ C.attracts_friends() ],
			'marigold': [ C.attracts_friends() ],
			'sunflower': [ C.sunlight_competition() ],
			'squash': [ C.resource_competition() ],
			'tomato': [ C.sunlight_competition() ],
			'peppers': [ C.sunlight_competition() ],
			'potato': [ C.same_pests() ]
		},
		'parsley': {
			'corn': [ C.attracts_friends() ],
			'beans': [ C.attracts_friends() ],
			'peppers': [ C.repels_pests() ],
			'chives': [ C.attracts_friends() ],
			'carrots': [ C.same_pests() ],
			'garlic': [ C.bad_allelopathy() ],
			'onion': [ C.bad_allelopathy() ],
			'mint': [ C.overgrowth_competition() ]
		},
		'basil': {
			'chives': [ C.repels_pests() ],
			'garlic': [ C.repels_pests() ],
			'fennel': [ C.repels_pests() ],
			'marigold': [ C.repels_pests() ],
			'onion': [ C.repels_pests() ],
			'parsley': [  ], # Similar preferred environment, fill in more specifically later
			'peppers': [ C.repels_pests() ]
		},
		'garlic': {
			'carrots': [ C.repels_pests() ],
			'nasturtium': [ C.supress_weeds() ],
			'marigold': [ C.repels_pests() ]
		},
		'chives': {
			'carrots': [ C.repels_pests() ],
			'peas': [ C.repels_pests() ],
			'peppers': [ C.repels_pests() ],
			'potato': [  ] # Nothing particular, chives just have short roots so there's no root disruption
		},
		'sunflower': {
			'tomato': [ C.attracts_friends() ],
			'peppers': [ C.repels_pests() ],
			'onion': [ C.repels_pests() ],
			'garlic': [ C.repels_pests() ],
			'chives': [ C.repels_pests() ],
			'peas': [ C.provides_shade() ],
			'mint': [ C.repels_pests() ],
			'basil': [ C.repels_pests() ],
			'potato': [ C.same_pests() ],
			'corn': [ C.sunlight_competition() ],
			'fennel': [ C.bad_allelopathy() ],
			'squash': [ C.resource_competition() ],
			'watermelon': [ C.resource_competition() ]
		},
		'kohlrabi': {
			'onion': [ C.repels_pests() ],
			'garlic': [ C.repels_pests() ],
			'potato': [ C.soil_loosener() ],
			'beans': [ C.bad_allelopathy() ],
			'tomato': [ C.bad_allelopathy() ],
			'watermelon': [ C.sunlight_competition() ],
			'squash': [ C.sunlight_competition() ],
			'sunflower': [ C.sunlight_competition() ]
		},
		'nasturtium': {
			'peppers': [ C.repels_pests() ],
			'marigold': [ C.repels_pests() ],
			'fennel': [ C.bad_allelopathy() ]
		},
		'fennel': {
			'beans': [ C.bad_allelopathy() ],
			'kohlrabi': [ C.bad_allelopathy() ],
			'peppers': [ C.bad_allelopathy() ]
		},
		'carrots': {
			'peas': [ C.nitrogen_fixer() ],
			'parsley': [ C.attracts_friends() ],
			'fennel': [ C.bad_allelopathy() ]
		},
		'peas': {
			'corn': [ C.nitrogen_fixer() ],
			'basil': [ C.repels_pests() ],
			'nasturtium': [ C.sacrificial_crop() ],
			'marigold': [ C.sacrificial_crop() ],
			'garlic': [ C.bad_allelopathy() ],
			'chives': [ C.bad_allelopathy() ]
		},
		'peppers': {
			'tomato': [ C.provides_shade() ],
			'corn': [ C.provides_shade() ],
			'beans': [ C.nitrogen_fixer() ],
			'squash': [ C.supress_weeds() ],
			'peas': [ C.nitrogen_fixer() ],
			'garlic': [ C.repels_pests() ],
			'carrots': [ C.supress_weeds() ],
			'marigold': [ C.repels_pests() ],
			'kohlrabi': [  ], # Prefer different environments, fill out more specifically later
			'potato': [ C.same_pests() ]
		},
		'marigold': {

		}
	}
