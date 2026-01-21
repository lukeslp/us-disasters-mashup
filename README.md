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
  splits:
    - name: train
      num_examples: 54575
---

# US Disasters Mashup

Unified dataset of **54,575 disaster events** across four categories from US government sources.

## Categories

| Category | Records | Source | Date Range |
|----------|---------|--------|------------|
| Aviation Accidents | 32,410 | NTSB | 1962-present |
| Shipwrecks | 3,653 | NOAA AWOIS | Historical |
| Severe Storms | 14,770 | NOAA | 1950-2025 |
| Earthquakes | 3,742 | USGS | 2000-2025 |

## Schema

```json
{
  "category": "aviation_accident|shipwreck|storm|earthquake",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "name": "Event name or location",
  "date": "2023-01-15",
  "subcategory": "Specific type (e.g., Tornado, maritime)",
  "magnitude": 5.2,
  "fatalities": 0,
  "injuries": 0
}
```

## Data Quality

- All records have valid coordinates
- Coordinate precision: 6 decimal places
- Aviation accidents: 100% have NTSB event IDs
- Storms: Include fatalities, injuries, damage estimates
- Earthquakes: Include magnitude and depth

## Use Cases

- **Geospatial Analysis**: Map disaster hotspots and corridors
- **Temporal Analysis**: Identify seasonal and long-term trends
- **Risk Assessment**: Cross-reference with population data
- **Machine Learning**: Multi-class disaster classification
- **Visualization**: "Data is Beautiful" style presentations

## Sources

All data from US Government agencies (public domain):

- **NTSB**: https://www.ntsb.gov/safety/data
- **NOAA AWOIS**: https://www.nauticalcharts.noaa.gov/data/wrecks-and-obstructions.html
- **NOAA Storm Events**: https://www.ncdc.noaa.gov/stormevents/
- **USGS Earthquakes**: https://earthquake.usgs.gov/

## Distribution

- **Kaggle**: [lucassteuber/us-disasters-mashup](https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup)
- **HuggingFace**: [lukeslp/us-disasters-mashup](https://huggingface.co/datasets/lukeslp/us-disasters-mashup)
- **GitHub Gist**: [Demo Notebook](https://gist.github.com/lukeslp/1bf1ce9d0e4bedce40be25d82b986a08)

## Author

Luke Steuber | @lukesteuber.com (Bluesky)

## Structured Data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "US Disasters Mashup",
  "description": "Unified dataset of 54,575 disaster events across four categories from US government sources: aviation accidents (NTSB), shipwrecks (NOAA AWOIS), severe storms (NOAA), and earthquakes (USGS).",
  "url": "https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup",
  "sameAs": "https://huggingface.co/datasets/lukeslp/us-disasters-mashup",
  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
  "creator": {
    "@type": "Person",
    "name": "Luke Steuber",
    "url": "https://lukesteuber.com"
  },
  "keywords": ["disasters", "aviation accidents", "shipwrecks", "storms", "earthquakes", "geospatial", "united states"],
  "temporalCoverage": "1950/2025",
  "spatialCoverage": {
    "@type": "Place",
    "name": "United States"
  },
  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://www.kaggle.com/datasets/lucassteuber/us-disasters-mashup"
    }
  ]
}
```
