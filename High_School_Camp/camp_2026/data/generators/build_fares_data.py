#!/usr/bin/env python3
"""Generate synthetic_fares.csv: invented boda-boda trip fares for the ML project weeks.

Why this exists: synthetic_homes.csv is generated from an easy formula, so every
student's model looks excellent. Fares carry real-looking noise, so a model beats
its baseline by a moderate margin and a weak feature (rain) shows up as weak.
`tip_ugx` is a deliberate leakage column: it is only known after the trip and it
tracks the fare, so a model that uses it looks better and predicts nothing.

Everything is invented. No real trips, riders or prices. Seeded for repeatability.
Usage: python3 build_fares_data.py
"""
import csv, os, random
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # camp_2026/data
rnd = random.Random(20261031)
rows = []
for i in range(1, 151):
    d = round(rnd.uniform(0.5, 15.0), 1)
    rush = 1 if rnd.random() < 0.35 else 0
    rain = 1 if rnd.random() < 0.25 else 0
    fare = 1000 + 900 * d + 1500 * rush + 600 * rain + rnd.gauss(0, 3000)
    fare = max(1000, int(round(fare / 100.0)) * 100)
    tip = int(round(max(0.0, fare * 0.06 + rnd.gauss(0, 150)) / 100.0)) * 100
    rows.append((i, d, rush, rain, fare, tip))
with open(os.path.join(HERE, "synthetic_fares.csv"), "w", newline="\n") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["trip_id", "distance_km", "rush_hour", "raining", "fare_ugx", "tip_ugx"])
    w.writerows(rows)
print("wrote synthetic_fares.csv", len(rows), "rows")
