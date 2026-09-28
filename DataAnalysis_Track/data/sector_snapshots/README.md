# Fixed sector data for the independent track

Use these local files during class. `manifest.json` records retrieval time, exact source URLs, transformations and SHA-256 hashes. Keep the original snapshot for an assessment window; upstream revisions must not silently change its answer key.

- **Banking / telecom:** `bank-full.csv` uses semicolons and has 45,211 rows and 17 columns. This is the older full Bank Marketing variant. Cite [Moro, Rita and Cortez, UCI Bank Marketing](https://doi.org/10.24432/C5K306), CC BY 4.0. `bank-names.txt` is the supplied dictionary. Records concern Portuguese bank campaigns; they do not establish Ugandan customer behaviour. Call duration is unavailable before a call and cannot support pre-call targeting.
- **Energy / manufacturing:** `ai4i2020.csv` has 10,000 rows and 14 columns. Cite [AI4I 2020, UCI](https://doi.org/10.24432/C5HS5C), CC BY 4.0. It is **synthetic**, not measured plant data. Temperature is kelvin, torque Nm, speed rpm and tool wear minutes. Failure-mode columns describe outcomes and must not be presented as prediction-time inputs.
- **Public sector / development:** `uganda_gdp_2000_2023.csv` selects Uganda's annual GDP in current US dollars for 2000–2023 from the [World Bank indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures). The original JSON response is retained. Years are sorted, nulls remain blank and no values were imputed. Cite World Bank, World Development Indicators, indicator `NY.GDP.MKTP.CD`, and the retrieval date in the manifest. Apply the [World Bank data licence and additional terms](https://datacatalog.worldbank.org/public-licenses). This series is nominal, exchange-rate-sensitive GDP; it does not measure real growth, household income or health outcomes.

The snapshots provide reproducible inputs. They do not, by themselves, validate a learner's interpretation or a Power BI model. Later assessment forms remain subject to calibration and release checks.

To verify downloaded files without contacting the internet:

```sh
.iuea-grader-env/bin/python scripts/verify_sector_snapshots.py
```

`stage_sector_snapshots.py` is the explicit download/retrieval command. It refuses to replace a file whose bytes changed; create a separately versioned snapshot before adopting an upstream revision.
