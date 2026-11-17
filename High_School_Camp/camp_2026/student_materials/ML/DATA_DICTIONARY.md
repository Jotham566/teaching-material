# Supplied teaching data

All files are generated synthetic examples. They are not observations of actual shops, trips or housing, and contain no learner records. Generators use fixed seeds so every number can be reproduced and checked. No claim about real demand, prices, fares or rents can be drawn from them.

## camp_shop.csv

60 sales records across 20 illustrative December dates. `sale_id`: unique identifier. `date`: YYYY-MM-DD text. `item`: Book, Pen or Juice. `units`: whole items sold. `unit_price_ugx`: UGX per item. Revenue is units multiplied by unit price. Costs are absent, so profit cannot be calculated. The file is small on purpose so that answers can be checked by hand: 277 units, UGX 550,000 revenue (Book 297,000, Juice 150,000, Pen 103,000). Pen sells the most units and Book earns the most money.

## synthetic_homes.csv (ML)

120 invented independent home records. `home_id`: identifier, exclude from model inputs. `area_m2`: floor area in square metres. `rooms`: number of rooms. `rent_ugx`: invented monthly rent in UGX. Features: area_m2 and rooms. Target: rent_ugx. The generating formula deliberately creates an easy learnable relationship, so every model scores well. Performance is a workflow exercise and says nothing about a market.

## synthetic_fares.csv (ML)

150 invented boda-boda trips. `trip_id`: identifier, exclude from model inputs. `distance_km`: trip distance. `rush_hour` and `raining`: 1 for yes and 0 for no. `fare_ugx`: invented fare in UGX. `tip_ugx`: invented tip. Features: distance_km, rush_hour, raining. Target: fare_ugx. The fares carry real-looking noise, so a model beats its baseline by a moderate margin and a weak feature such as rain shows up as weak. `tip_ugx` is a deliberate leakage column: it is only known after the trip and tracks the fare, so a model that uses it looks better and predicts nothing. Generator: build_fares_data.py.

## Iris (ML)

Classification uses `sklearn.datasets.load_iris`, bundled with scikit-learn after installation. Inputs are four flower measurements in centimetres; the target is a species encoded as 0, 1 or 2. Display `data.feature_names` and `data.target_names` in class to connect codes with names. This is a historical teaching dataset. Source: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
