# Data

All data is generated and synthetic. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the columns and what each file is for.

| Path | What it holds |
|---|---|
| camp_shop.csv, synthetic_homes.csv | The 60-row practice shop and 120 invented homes. Written by `build/build_camp.py`. |
| synthetic_fares.csv | 150 invented boda-boda trips with noise and a leakage column. Written by `generators/build_fares_data.py`. |
| sunrise/ | The Sunrise Shops dataset for Python for Data Analysis, its answer key and its [dictionary](sunrise/DATA_DICTIONARY.md). The SQLite file is for the professional courses. |
| generators/ | `build_sunrise_data.py`, `verify_sunrise_data.py` (32 checks) and `build_fares_data.py`. Run from this folder, for example `python3 generators/verify_sunrise_data.py`. |
