export default {
  plants: [
    {
      name: 'Corn (modern hybrids)',
      species: 'zea mays',
      references: [
        'Bender et al., 2013',
        'Shorter, 2014'
      ],
      conversions: {
        'lb/bu': 70,
        'bu/A': 230
      },
      pH: [5.8, 6.8],
      uptake: [
        {nutrient: 'N', rate: '256 lb/A'},
        {nutrient: 'P2O5', rate: '101 lb/A'},
        {nutrient: 'K2O', rate: '180 lb/A'},
        {nutrient: 'S', rate: '23 lb/A'},
        {nutrient: 'Zn', rate: '7.1 oz/A'},
        {nutrient: 'B', rate: '1.2 oz/A'}
      ]
    },
    {
      name: 'Zucchini',
      species: 'cucurbita pepo',
      references: [
        'Rouphael et al., 2003',
        'Fritz and Rosen, 2018'
      ],
      pH: [6.0, 6.5],
      uptake: [
        {nutrient: 'N', rate: '103 g/kg'},
        {nutrient: 'P', rate: '18.3 g/kg'},
        {nutrient: 'K', rate: '174.4 g/kg'},
        {nutrient: 'Ca', rate: '51.3 g/kg'},
        {nutrient: 'Mg', rate: '24.8 g/kg'}
      ]
    },
    {
      name: 'Butternut Squash',
      species: 'cucurbita moschata',
      references: [
        'Department of Agriculture, Forestry and Fisheries; 2011',
        'Starke Ayres, 2019',
        'Napier, 2009'
      ],
      conversions: {
        'kg/plant': 1.4,
        'plant/ha': 10000
      },
      pH: [5.6, 6.5],
      uptake: [
        {nutrient: 'N', rate: '160 kg/ha'},
        {nutrient: 'P', rate: '20 kg/ha'},
        {nutrient: 'K', rate: '20 kg/ha'}
      ]
    },
    {
      name: 'Muskmelon',
      species: 'cucumis melo',
      references: [
        'Rincon-Sanchez et al., 1998',
        'Steve Albert, 2015'
      ],
      pH: [5.5, 6.5],
      uptake: [
        {nutrient: 'N', rate: '3.8 kg/t'},
        {nutrient: 'P', rate: '0.63 kg/t'},
        {nutrient: 'K', rate: '7.8 kg/t'},
        {nutrient: 'Ca', rate: '3.1 kg/t'},
        {nutrient: 'Mg', rate: '1.6 kg/t'}
      ]
    },
    {
      name: 'Watermelon',
      species: 'citrullus lanatus',
      references: [
        'Quattrucci, 2000',
        'Steve Albert, 2015'
      ],
      pH: [5.5, 6.5],
      uptake: [
        {nutrient: 'N', rate: '1.5 kg/t'},
        {nutrient: 'P', rate: '0.3 kg/t'},
        {nutrient: 'K', rate: '2.6 kg/t'},
        {nutrient: 'Ca', rate: '0.75 kg/t'},
        {nutrient: 'Mg', rate: '0.15 kg/t'}
      ]
    }
  ]
}
