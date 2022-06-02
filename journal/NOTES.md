# Units
Nutrient uptake data often comes in varying units, usually pound per acre (lb/A) or pound per bushel (lb/bu).
Sometimes it'll be logged as percentage of crop biomass.

## Conversion
Convert uptake data with the following:
- Identify bu/A
- Identify pound of crop biomass per bushel
- Divide until you end without units (weight of nutrient per weight of crop biomass)
- You'll end with some fraction (convert to percentage) of crop biomass

Note: You'll need to store average biomass of a single unit of each crop

## Standardized units in data
- `height` (meters)

# Additional constraints
- Each species in a companionship fills 1 of 7 (or more) layers, also known as forest layers
  - Canopy layer is over 30 feet (9 meters), sub-canopy layer is 10 - 30 feet, and shrub layer is up to 10 feet (3 meters)
- [Soil drainage requirements](https://cteco.uconn.edu/guides/Soils_Drainage.htm): excessively drained, somewhat excessively drained, well drained, moderately well drained, somewhat poorly drained, poorly drained, very poorly drained
- [Sunlight requirements](https://www.johnson.k-state.edu/lawn-garden/agent-articles/miscellaneous/defining-sun-requirements-for-plants.html): full sun, light shade, partial shade, full shade, dense shade
- [Water requirements](https://www.ladwp.cafriendlylandscaping.com/Garden-Resources/WaterNeeds.php): high, moderate, low, very low

# Metabolism
- **Metabolic pathway** - a linked series of chemical reactions occurring within a cell
- **Metabolite** - an intermediate result of a metabolic pathway
- **Metabolomics** - the comprehensive measurement of all metabolites in a biological specimen

# Plant Taxonomy
As defined by the [International Code of Nomenclature on Algae, Fungi and Plants](https://en.wikipedia.org/wiki/International_Code_of_Nomenclature_for_algae,_fungi,_and_plants):
- `Kingdom`
- `Division`
- `Class`
- `Order`
- `Family`
- `Genus`
- `Species`

There are only 620 plant families in existence.

# Growth Habits
- `Forb (herb)` An herbaceous (non woody) plant without grass-like characteristics
- `Graminoid` Grass or grass-like plant
- `Lichenous` Recognized as single plant but is living in symbiosis with a fungus
- `Nonvascular` Terrestrial, herbaceous green plant often attached to some object
- `Shrub` Perennial woody plant that is usually multi-stemmed and under 5 meters tall
- `Subshrub` Low growing shrub never exceeding 1 meter
- `Tree` Perennial woody plant usually with single stem and over 5 meters tall
- `Vine` Twining plant with long stems, can be woody or herbaceous

# Useful Python links
- [Packaging Python for Pip](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Modules vs. packages](https://docs.python.org/3/tutorial/modules.html)
- [Pylint](https://pylint.org/)
- [Python style guide](https://www.python.org/dev/peps/pep-0008/)