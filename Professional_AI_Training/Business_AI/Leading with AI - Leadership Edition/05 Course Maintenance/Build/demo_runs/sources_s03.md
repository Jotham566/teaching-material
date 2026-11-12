# Sources checked for Session 3 (6 November 2026)

- scikit-learn model evaluation guide, https://scikit-learn.org/stable/modules/model_evaluation.html (read 6 Nov 2026): precision = tp / (tp + fp); recall = tp / (tp + fn); F1 is the weighted harmonic mean of precision and recall with beta 1; ROC AUC is the area under the ROC curve (true positive rate against false positive rate across thresholds). Used for the definitions on the slides.
- The plain-words reading of AUC on the ROC slide (the chance that a random late invoice scores higher than a random on-time one) is the standard rank interpretation of ROC AUC; it was not separately fetched. The page above was read only in part (the first 100,000 characters).
- Not stated on any slide because not verified: any industry statistic on late-payment rates, any benchmark value for a "good" AUC (the notes say what 0.5 and 1.0 mean and say a good value depends on the task).
- All data on the slides are invented (Nile Valley Foods is fictional) and come from `demo_runs/s03/`.
