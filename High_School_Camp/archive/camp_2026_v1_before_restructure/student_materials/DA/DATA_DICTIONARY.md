# Supplied teaching data

Both CSV files are generated synthetic examples, not observations of actual shops or housing. The generator uses a fixed seed for reproducible checking. They contain no learner records. No claim about real demand, prices or rents can be inferred from them.

## camp_shop.csv and camp_shop.sqlite

60 sales records across 20 illustrative December dates. `sale_id`: unique record identifier. `date`: YYYY-MM-DD date string. `item`: Book, Pen or Juice. `units`: whole items sold. `unit_price_ugx`: UGX per item. Revenue is units multiplied by unit price. Costs are absent, so profit cannot be calculated. The SQLite products table has one unique item key and its category. A matching item connects sales to products. No intentionally missing values or duplicate IDs in this clean file; cleaning mistakes are introduced separately in the worked lessons.

## synthetic_homes.csv

120 invented independent home records. `home_id`: identifier, exclude from model inputs. `area_m2`: floor area in square metres. `rooms`: whole-number room count. `rent_ugx`: invented monthly rent in UGX. Features: area_m2 and rooms. Target: rent_ugx. The generation formula deliberately creates an easy learnable relationship; performance is a workflow exercise, not validation of a market model. Use a held-out test and report this limitation.

## Iris

ML classification uses `sklearn.datasets.load_iris`, bundled with scikit-learn after installation. Inputs are four flower measurements in centimetres; target is a species category encoded as 0, 1 or 2. Display `data.feature_names` and `data.target_names` in class to connect codes with names. This is a historical teaching dataset, not student data. Source documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
