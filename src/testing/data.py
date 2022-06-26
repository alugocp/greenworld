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
			'basil': [  ],
			'beans': [  ],
			'carrots': [  ],
			'chives': [  ],
			'garlic': [  ],
			'marigold': [  ],
			'mint': [  ],
			'nasturtium': [  ],
			'onion': [  ],
			'parsley': [  ],
			'squash': [  ],
			'corn': [  ],
			'peppers': [  ],
			'potato': [  ],
			'fennel': [  ]
		},
		'onion': {
			'peppers': [  ],
			'carrots': [  ],
			'parsley': [  ],
			'beans': [  ],
			'peas': [  ],
			'garlic': [  ],
			'chives': [  ]
		},
		'corn': {
			'squash': [  ],
			'beans': [  ],
			'watermelon': [  ],
			'marigold': [  ],
			'mint': [  ],
			'nasturtium': [  ],
			'sunflower': [  ],
			'fennel': [  ]
		},
		'squash': {
			'nasturtium': [  ],
			'beans': [  ],
			'marigold': [  ],
			'peas': [  ],
			'mint': [  ]
		},
		'beans': {
			'nasturtium': [  ],
			'peas': [  ],
			'carrots': [  ],
			'chives': [  ],
			'garlic': [  ],
			'peppers': [  ],
			'sunflower': [  ]
		},
		'mint': {
			'beans': [  ],
			'carrots': [  ],
			'onion': [  ],
			'peas': [  ],
			'peppers': [  ]
		},
		'watermelon': {
			'onion': [  ],
			'garlic': [  ],
			'chives': [  ],
			'beans': [  ],
			'carrots': [  ],
			'mint': [  ],
			'nasturtium': [  ],
			'marigold': [  ],
			'sunflower': [  ],
			'squash': [  ],
			'tomato': [  ],
			'peppers': [  ],
			'potato': [  ]
		},
		'parsley': {
			'corn': [  ],
			'beans': [  ],
			'peppers': [  ],
			'chives': [  ],
			'carrots': [  ],
			'garlic': [  ],
			'onion': [  ],
			'mint': [  ]
		},
		'basil': {
			'chives': [  ],
			'garlic': [  ],
			'fennel': [  ],
			'marigold': [  ],
			'onion': [  ],
			'parsley': [  ],
			'peppers': [  ]
		},
		'garlic': {
			'carrots': [  ],
			'nasturtium': [  ],
			'marigold': [  ]
		},
		'chives': {
			'carrots': [  ],
			'peas': [  ],
			'peppers': [  ],
			'potato': [  ]
		},
		'sunflower': {
			'tomato': [  ],
			'peppers': [  ],
			'onion': [  ],
			'garlic': [  ],
			'chives': [  ],
			'peas': [  ],
			'mint': [  ],
			'basil': [  ],
			'potato': [  ],
			'corn': [  ],
			'fennel': [  ],
			'squash': [  ],
			'watermelon': [  ]
		},
		'kohlrabi': {
			'onion': [  ],
			'garlic': [  ],
			'potato': [  ],
			'beans': [  ],
			'tomato': [  ],
			'watermelon': [  ],
			'squash': [  ],
			'sunflower': [  ]
		},
		'nasturtium': {
			'peppers': [  ],
			'marigold': [  ],
			'fennel': [  ]
		},
		'fennel': {
			'beans': [  ],
			'kohlrabi': [  ],
			'peppers': [  ]
		},
		'carrots': {
			'peas': [  ],
			'parsley': [  ],
			'fennel': [  ]
		},
		'peas': {
			'corn': [  ],
			'basil': [  ],
			'nasturtium': [  ],
			'marigold': [  ],
			'garlic': [  ],
			'chives': [  ]
		},
		'peppers': {
			'tomato': [  ],
			'corn': [  ],
			'beans': [  ],
			'squash': [  ],
			'peas': [  ],
			'garlic': [  ],
			'carrots': [  ],
			'marigold': [  ],
			'kohlrabi': [  ],
			'potato': [  ]
		},
		'marigold': {

		}
	}
