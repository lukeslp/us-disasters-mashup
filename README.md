---
license: cc0-1.0
task_categories:
  - feature-extraction
  - time-series-forecasting
tags:
  - disasters
  - aviation
  - maritime
  - weather
  - seismic
  - geospatial
  - united-states
  - safety
size_categories:
  - 10K<n<100K
dataset_info:
  features:
    - name: category
      dtype: string
    - name: latitude
      dtype: float64
    - name: longitude
      dtype: float64
    - name: name
      dtype: string
    - name: date
      dtype: string
    - name: subcategory
      dtype: string
    - name: magnitude
      dtype: float64
    - name: fatalities
      dtype: int64
    - name: injuries
      dtype: int64
    - name: damage
      dtype: string
    - name: state
      dtype: string
    - name: aircraft_type
      dtype: string
    - name: event_id
      dtype: string
    - name: vessel_type
      dtype: string
    - name: depth_km
      dtype: float64
  splits:
    - name: train
      num_examples: 48592
---

# US Disasters Mashup

**48,592 disaster events** pulled from four US government databases into one flat JSON file. Plane crashes, shipwrecks, tornadoes, earthquakes -- all geocoded and categorized.

## What's In It

| Category | Records | Source | Date Range |
|----------|---------|--------|------------|
| Aviation Accidents | 26,427 | NTSB | 1974-2018 |
| Severe Storms | 14,770 | NOAA Storm Events | 1950-2025 |
| Earthquakes | 3,742 | USGS | 2020-2025 |
| Shipwrecks | 3,653 | NOAA AWOIS | Historical (1600s-1970s) |

## Fields

Every record has core fields (category, latitude, longitude, name, date, subcategory). Additional fields depend on the category:

| Field | Coverage | Which Categories |
|-------|----------|-----------------|
| `category` | 100% | All |
| `latitude` / `longitude` | 100% | All |
| `name` | 100% | All -- event description or location |
| `subcategory` | 100% | Tornado, Flash Flood, seismic, maritime, aviation, etc. |
| `date` | 94% | All except some historical shipwrecks |
| `aircraft_type` | 59% | Aviation only |
| `event_id` | 59% | Aviation only (NTSB event IDs) |
| `magnitude` | 20% | Storms (Fujita/EF scale) + Earthquakes (Richter) |
| `fatalities` | 27% | Storms |
| `injuries` | 27% | Storms |
| `damage` | 26% | Storms (text format: "250K", "1.5M") |
| `state` | 27% | Storms |
| `vessel_type` | <1% | Shipwrecks (sparse) |

### Example Records

**Storm:**
```json
{
  "category": "storm",
  "latitude": 34.88,
  "longitude": -99.28,
  "name": "Tornado in OKLAHOMA, KIOWA",
  "date": "1950-04-28",
  "subcategory": "Tornado",
  "magnitude": "0",
  "fatalities": "1",
  "injuries": "1",
  "damage": "250K",
  "state": "OKLAHOMA"
}
```

**Aviation:**
```json
{
  "category": "aviation_accident",
  "latitude": 20.000833,
  "longitude": -155.6675,
  "name": "Aviation Accident - SCHLEICHER ASH25M",
  "date": "2012-01-01",
  "subcategory": "aviation",
  "aircraft_type": "SCHLEICHER ASH25M",
  "event_id": "20121010X84549"
}
```

## Known Quirks

A few things worth knowing if you're working with this data:

- **Aviation dates are year-only.** Aviation records show `YYYY-01-01`. The actual dates are embedded in the event IDs (e.g., `20121010X84549` = Oct 10, 2012) but the date field just has the year.
- **Earthquake dates are ISO format** (`YYYY-MM-DD`), converted from Unix timestamps.
- **Aviation records are deduplicated** on `event_id` (5,983 duplicates removed from source overlaps).
- **Coordinates extend beyond CONUS.** Some records are in Hawaii, Alaska, territories, or international waters. Expected for aviation and maritime data.
- **`depth_km` is always null.** The field exists in the schema but was never populated.

## Loading

```python
import json

with open("disasters_mashup.json") as f:
    disasters = json.load(f)

# Filter by category
storms = [d for d in disasters if d["category"] == "storm"]
aviation = [d for d in disasters if d["category"] == "aviation_accident"]

# Deduplicate aviation (optional)
seen = set()
unique_aviation = []
for d in aviation:
    if d.get("event_id") not in seen:
        seen.add(d.get("event_id"))
        unique_aviation.append(d)
```

## Sources

All public domain, from US government agencies:

- [NTSB Aviation Safety Data](https://www.ntsb.gov/safety/data)
- [NOAA AWOIS Wrecks & Obstructions](https://www.nauticalcharts.noaa.gov/data/wrecks-and-obstructions.html)
- [NOAA Storm Events Database](https://www.ncdc.noaa.gov/stormevents/)
- [USGS Earthquake Hazards](https://earthquake.usgs.gov/)

## Where to Get It

- **GitHub**: [lukeslp/us-disasters-mashup](https://github.com/lukeslp/us-disasters-mashup)
- **HuggingFace**: [lukeslp/us-disasters-mashup](https://huggingface.co/datasets/lukeslp/us-disasters-mashup)
- **Kaggle**: [lucassteuber/us-disasters-mashup](https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup)
- **Demo Notebook**: [Jupyter on GitHub Gist](https://gist.github.com/lukeslp/1bf1ce9d0e4bedce40be25d82b986a08)

## License

CC0 1.0 (Public Domain). All source data comes from US government agencies.

## Author

**Luke Steuber**
- Website: [lukesteuber.com](https://lukesteuber.com)
- Bluesky: [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)

## Citation

```bibtex
@dataset{steuber2026disasters,
  title={US Disasters Mashup},
  author={Steuber, Luke},
  year={2026},
  publisher={GitHub/HuggingFace/Kaggle},
  url={https://github.com/lukeslp/us-disasters-mashup}
}
```

## Structured Data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "US Disasters Mashup",
  "description": "54,575 disaster events from four US government databases (NTSB aviation accidents, NOAA shipwrecks, NOAA severe storms, USGS earthquakes) unified into a single geocoded JSON file.",
  "url": "https://github.com/lukeslp/us-disasters-mashup",
  "sameAs": [
    "https://huggingface.co/datasets/lukeslp/us-disasters-mashup",
    "https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup"
  ],
  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
  "creator": {
    "@type": "Person",
    "name": "Luke Steuber",
    "url": "https://lukesteuber.com"
  },
  "keywords": ["disasters", "aviation accidents", "shipwrecks", "storms", "earthquakes", "geospatial", "united states"],
  "temporalCoverage": "1600/2025",
  "spatialCoverage": {
    "@type": "Place",
    "name": "United States"
  },
  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://github.com/lukeslp/us-disasters-mashup"
    }
  ]
}
```
