# This file defines expected GreenWorld output for various selected companion plants.
# Every plant listed here should also be listed in src/testing/plants.txt.
# TODO remove src/tsting/(anti)*companions.txt when this file is fully implemented.
from greenworld.model.suggestion import Suggestion as S

def generate_validation_data():
	return {
		'potato': {
			'garlic': [ S.repels_pests() ],
			'onion': [ S.repels_pests() ],
			'peas': [ S.nitrogen_fixer() ],
			'beans': [ S.nitrogen_fixer() ],
			'corn': [ S.provides_shade() ],
			'basil': [ S.repels_pests() ],
			'parsley': [ S.sacrificial_crop() ],
			'marigold': [ S.sacrificial_crop() ],
			'nasturtium': [ S.sacrificial_crop() ],
			'squash': [ S.resource_competition(), S.similar_diseases() ],
			'carrots': [ S.root_disruption() ],
			'sunflower': [ S.bad_allelopathy() ],
			'fennel': [ S.bad_allelopathy() ]
		},
		'tomato': {
			'basil': [ S.repels_pests() ],
			'beans': [  ], # Similar preferred environment, fill in more specifically later
			'carrots': [ S.soil_loosener() ],
			'chives': [ S.good_allelopathy() ],
			'garlic': [ S.repels_pests() ],
			'marigold': [ S.repels_pests() ],
			'mint': [ S.good_allelopathy() ],
			'nasturtium': [ S.sacrificial_crop() ],
			'onion': [ S.repels_pests() ],
			'parsley': [ S.good_allelopathy() ],
			'squash': [  ], # Unknown reasons, look into later
			'corn': [ S.same_pests() ],
			'peppers': [ S.same_pests() ],
			'potato': [ S.same_pests() ],
			'fennel': [ S.bad_allelopathy() ]
		},
		'onion': {
			'peppers': [ S.repels_pests() ],
			'carrots': [ S.repels_pests() ],
			'parsley': [ S.repels_pests() ],
			'beans': [ S.bad_allelopathy() ],
			'peas': [ S.bad_allelopathy() ],
			'garlic': [ S.same_pests() ],
			'chives': [ S.same_pests() ]
		},
		'corn': {
			'squash': [ S.supress_weeds() ],
			'beans': [ S.nitrogen_fixer() ],
			'watermelon': [ S.supress_weeds() ],
			'marigold': [ S.attracts_friends() ],
			'mint': [ S.repels_pests() ],
			'nasturtium': [ S.sacrificial_crop() ],
			'sunflower': [ S.attracts_friends() ],
			'fennel': [ S.bad_allelopathy() ]
		},
		'squash': {
			'nasturtium': [ S.attracts_friends(), S.sacrificial_crop() ],
			'beans': [ S.nitrogen_fixer(), S.repels_pests() ],
			'marigold': [ S.repels_pests() ],
			'peas': [ S.nitrogen_fixer() ],
			'mint': [ S.attracts_friends() ]
		},
		'beans': {
			'nasturtium': [ S.sacrificial_crop() ],
			'peas': [ S.nitrogen_fixer() ],
			'carrots': [ S.nitrogen_fixer(), S.repels_pests() ],
			'chives': [ S.bad_allelopathy() ],
			'garlic': [ S.bad_allelopathy() ],
			'peppers': [ S.vine_competition() ],
			'sunflower': [ S.bad_allelopathy() ]
		},
		'mint': {
			'beans': [ S.repels_pests() ],
			'carrots': [ S.repels_pests() ],
			'onion': [ S.repels_pests() ],
			'peas': [ S.repels_pests() ],
			'peppers': [ S.repels_pests() ]
		},
		'watermelon': {
			'onion': [ S.repels_pests() ],
			'garlic': [ S.repels_pests() ],
			'chives': [ S.repels_pests() ],
			'beans': [ S.nitrogen_fixer() ],
			'carrots': [ S.soil_loosener() ],
			'mint': [ S.repels_pests() ],
			'nasturtium': [ S.attracts_friends() ],
			'marigold': [ S.attracts_friends() ],
			'sunflower': [ S.sunlight_competition() ],
			'squash': [ S.resource_competition() ],
			'tomato': [ S.sunlight_competition() ],
			'peppers': [ S.sunlight_competition() ],
			'potato': [ S.same_pests() ]
		},
		'parsley': {
			'corn': [ S.attracts_friends() ],
			'beans': [ S.attracts_friends() ],
			'peppers': [ S.repels_pests() ],
			'chives': [ S.attracts_friends() ],
			'carrots': [ S.same_pests() ],
			'garlic': [ S.bad_allelopathy() ],
			'onion': [ S.bad_allelopathy() ],
			'mint': [ S.overgrowth_competition() ]
		},
		'basil': {
			'chives': [ S.repels_pests() ],
			'garlic': [ S.repels_pests() ],
			'fennel': [ S.repels_pests() ],
			'marigold': [ S.repels_pests() ],
			'onion': [ S.repels_pests() ],
			'parsley': [  ], # Similar preferred environment, fill in more specifically later
			'peppers': [ S.repels_pests() ]
		},
		'garlic': {
			'carrots': [ S.repels_pests() ],
			'nasturtium': [ S.supress_weeds() ],
			'marigold': [ S.repels_pests() ]
		},
		'chives': {
			'carrots': [ S.repels_pests() ],
			'peas': [ S.repels_pests() ],
			'peppers': [ S.repels_pests() ],
			'potato': [  ] # Nothing particular, chives just have short roots so there's no root disruption
		},
		'sunflower': {
			'tomato': [ S.attracts_friends() ],
			'peppers': [ S.repels_pests() ],
			'onion': [ S.repels_pests() ],
			'garlic': [ S.repels_pests() ],
			'chives': [ S.repels_pests() ],
			'peas': [ S.provides_shade() ],
			'mint': [ S.repels_pests() ],
			'basil': [ S.repels_pests() ],
			'potato': [ S.same_pests() ],
			'corn': [ S.sunlight_competition() ],
			'fennel': [ S.bad_allelopathy() ],
			'squash': [ S.resource_competition() ],
			'watermelon': [ S.resource_competition() ]
		},
		'kohlrabi': {
			'onion': [ S.repels_pests() ],
			'garlic': [ S.repels_pests() ],
			'potato': [ S.soil_loosener() ],
			'beans': [ S.bad_allelopathy() ],
			'tomato': [ S.bad_allelopathy() ],
			'watermelon': [ S.sunlight_competition() ],
			'squash': [ S.sunlight_competition() ],
			'sunflower': [ S.sunlight_competition() ]
		},
		'nasturtium': {
			'peppers': [ S.repels_pests() ],
			'marigold': [ S.repels_pests() ],
			'fennel': [ S.bad_allelopathy() ]
		},
		'fennel': {
			'beans': [ S.bad_allelopathy() ],
			'kohlrabi': [ S.bad_allelopathy() ],
			'peppers': [ S.bad_allelopathy() ]
		},
		'carrots': {
			'peas': [ S.nitrogen_fixer() ],
			'parsley': [ S.attracts_friends() ],
			'fennel': [ S.bad_allelopathy() ]
		},
		'peas': {
			'corn': [ S.nitrogen_fixer() ],
			'basil': [ S.repels_pests() ],
			'nasturtium': [ S.sacrificial_crop() ],
			'marigold': [ S.sacrificial_crop() ],
			'garlic': [ S.bad_allelopathy() ],
			'chives': [ S.bad_allelopathy() ]
		},
		'peppers': {
			'tomato': [ S.provides_shade() ],
			'corn': [ S.provides_shade() ],
			'beans': [ S.nitrogen_fixer() ],
			'squash': [ S.supress_weeds() ],
			'peas': [ S.nitrogen_fixer() ],
			'garlic': [ S.repels_pests() ],
			'carrots': [ S.supress_weeds() ],
			'marigold': [ S.repels_pests() ],
			'kohlrabi': [  ], # Prefer different environments, fill out more specifically later
			'potato': [ S.same_pests() ]
		},
		'marigold': {

		}
	}
