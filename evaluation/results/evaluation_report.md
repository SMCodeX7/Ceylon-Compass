# CeylonCompass Quantitative Evaluation

## Evaluation Scope

The evaluation contains **30 fixed traveller scenarios** covering different interests, budgets, trip lengths, starting locations, crowd preferences, travel styles and transport modes.

Weather conditions in this benchmark are **deterministic synthetic forecasts**. They are used to evaluate the behaviour of the weather-aware planning pipeline reproducibly. They do not evaluate Open-Meteo forecast accuracy.

Preference score is an internal cosine-similarity indicator derived from the curated destination feature vectors. It must not be interpreted as human-labelled recommendation accuracy.

## Overall Results

| Metric | Result |
| --- | ---: |
| Mean preference similarity | 82.63% |
| Mean final recommendation score | 85.06% |
| Mean category diversity | 47.33% |
| Budget compliance rate | 96.67% |
| Duration compliance rate | 100.00% |
| Mean scheduled-destination coverage | 82.38% |
| Controlled-weather coverage | 100.00% |
| Mean controlled-weather score | 80.86% |
| Route structural validity rate | 100.00% |
| Mean OR-Tools distance saving vs nearest-neighbour | 4.47% |
| OR-Tools not-worse-than-baseline rate | 100.00% |

## Segment Results

| segment    |   scenario_count |   mean_preference_score |   mean_final_score |   budget_compliance_rate_pct |   scheduled_coverage_pct |   category_diversity_pct |   route_distance_saving_pct |
|:-----------|-----------------:|------------------------:|-------------------:|-----------------------------:|-------------------------:|-------------------------:|----------------------------:|
| Adventure  |                3 |                   81.38 |              84.46 |                       100    |                    80.95 |                    66.67 |                        4.31 |
| Beach      |                3 |                   76.1  |              80.82 |                        66.67 |                    76.19 |                    33.33 |                        0.02 |
| Culture    |                3 |                   89.63 |              89.3  |                       100    |                    80.95 |                    40    |                       11.75 |
| Hiking     |                3 |                   81.31 |              83.97 |                       100    |                    80.95 |                    60    |                        2.71 |
| Long Trip  |                3 |                   93.78 |              90.46 |                       100    |                   100    |                    40    |                        4.55 |
| Mixed      |                6 |                   81.67 |              84.66 |                       100    |                    92.86 |                    50    |                        5.1  |
| Nature     |                3 |                   76.71 |              82.19 |                       100    |                    90.48 |                    46.67 |                        4.86 |
| Short Trip |                3 |                   78.28 |              84.4  |                       100    |                    42.86 |                    46.67 |                        1.11 |
| Wildlife   |                3 |                   85.79 |              85.65 |                       100    |                    85.71 |                    40    |                        5.17 |

## Interpretation Rules

- **Preference similarity** measures alignment between a traveller interest vector and curated destination feature vectors.
- **Final recommendation score** is the weighted CeylonCompass ranking score, not a probability.
- **Budget compliance** is based on the current V1 cost model and its explicit cost assumptions.
- **Duration compliance** checks the current 8-hour daily activity limit. Travel time is not included in that daily limit.
- **Route distance** uses Haversine great-circle distance. It is not actual road-driving distance.
- **Route saving** compares the OR-Tools result against the project's nearest-neighbour baseline using the same selected destinations.
- **Controlled-weather score** measures planner behaviour under deterministic weather inputs rather than real forecast accuracy.

## Current Evaluation Limitations

1. The project does not yet contain human relevance labels, so metrics such as Precision@K, Recall@K or NDCG against human ground truth cannot be claimed.
2. Destination interest features are curated modelling inputs and should not be treated as objective labels.
3. The budget model contains transparent V1 assumptions rather than guaranteed current Sri Lankan market prices.
4. Haversine distances can underestimate actual road travel.
5. The itinerary activity-hour constraint does not yet include travel time.
6. Controlled synthetic weather is used for reproducibility in this benchmark.
