# CeylonCompass Destination Dataset

This dataset contains structured destination features used by the CeylonCompass recommendation and itinerary-planning system.

## Geographic Features

- `destination_id` - Unique destination identifier
- `name` - Destination name
- `district` - Sri Lankan administrative district
- `province` - Province
- `latitude` - Geographic latitude
- `longitude` - Geographic longitude
- `category` - Primary tourism category

## Planning Features

- `estimated_daily_cost_usd` - Approximate traveller cost associated with visiting the destination
- `recommended_duration_hours` - Suggested visit duration
- `crowd_level` - Relative crowd level from 1 to 5

## Interest Features

The following features use values from 0 to 5:

- `beach`
- `wildlife`
- `hiking`
- `nature`
- `culture`
- `history`
- `adventure`

Scoring:

- 0 = Not relevant
- 1 = Very low relevance
- 2 = Low relevance
- 3 = Moderate relevance
- 4 = High relevance
- 5 = Very high relevance

## Traveller Suitability Features

- `fitness_requirement` - Physical effort required, from 1 to 5
- `family_suitability` - Suitability for family travellers, from 1 to 5
- `best_months` - Recommended months for visiting the destination

## Data Methodology

Geographic and descriptive fields should be based on verifiable sources.

Subjective recommendation features such as nature relevance, adventure relevance, crowd level, and family suitability are curated features created specifically for CeylonCompass.

These values are not treated as objective ground truth. They are used as model inputs and will later be tested through recommendation-system evaluation.

## Feature Provenance

The dataset contains two types of variables.

### Externally Verifiable Features

These are checked against geographic and tourism references:

- destination name
- district
- province
- latitude
- longitude
- destination type/category

### CeylonCompass Curated Features

The following are initial modelling assumptions created for the recommendation system:

- estimated daily cost
- recommended duration
- crowd level
- interest relevance scores
- fitness requirement
- family suitability
- seasonal recommendation

These values are not considered objective ground truth.

They provide an initial feature representation that can be tested,
evaluated and refined as part of the recommender-system development process.
