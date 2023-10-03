# Scoring System
We generate reports for pairs of plants and then calculate compatibility scores based on that.
Report generation runs through a set of rules, where applicable rules are added to the report.

## Rules
There are 5 categories of rules:
- Compare nitrogen usage/fixation
- Check for ecological interactions between other species
- Check for allelopathic interactions between the two plants
- Make sure the preferred environments overlap (soil pH, drainage, and type)
- Compare the plants' sun/shade inputs (requirements) and outputs (provisions)

These are derived from literature on companion planting.

## Compatibility scores
Each rule (if applicable) provides a number between 1.0 (good companion) and -1.0 (bad companion).
A pair's compatibility score is the average of these numbers.
Neutral companions (with no applicable rules) are given a null score.

## Validation (ground truth data)
### Good pairs
- [Companion Plants for Aphid Pest Management](https://gettheresearch.org/search?q=companion_plant&zoom=10.3390%2Finsects8040112)
    - *Capsicum annuum* with *Allium schoenoprasum*
    - *Brassica oleracea (Bently F1)* with *Tagetes patula nana* and *Calendula officinalis*
    - *Nicotiana tabacum* with *Allium sativum*
    - *Solanum tuberosum* with *Allium sativum*
    - *Capsicum annuum* with *Ocimum basilicum*, *Rosmarinus officinalis*, and *Lavandula latifolia*
    - *Brassica oleracea* with *Allium cepa*
    - *Brassica oleracea* with *Secale cereal*
    - *Vicia faba* with *Satureja hortensis* and *Ocimum basilicum*
    - *Pyrus communis* with *Satureja hortensis* and *Ocimum basilicum*
    - *Brassica napus* with *Allium cepa* and *Allium sativum*
    - *Rosa chinensis* with *Tagetes patula*
    - *Hordeum vulgare* with *Cirsium vulgare*

- [Companion planting with French marigolds protects tomato plants from glasshouse whiteflies through the emission of airborne limonene](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0213071&type=printable)
    - *Solanum lycopersicum* with *Tagetes patula*
