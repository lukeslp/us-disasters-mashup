# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

48,592 disaster events from 4 US government databases merged into a single geocoded JSON file. Has its own git repo at `lukeslp/us-disasters-mashup`.

## Directory Layout

```
us-disasters-mashup/
├── disasters_mashup.json           # Main output (11.6 MB, 48,592 records)
├── disasters_mashup_metadata.json  # Schema and statistics
├── create_disaster_mashup.py       # Build script (merges 4 sources)
├── airplane_crashes_metadata.json  # Aviation source metadata
├── demo_notebook.ipynb             # Usage examples
├── dataset-metadata.json           # Kaggle metadata
├── HUGGINGFACE_README.md           # HF dataset card
├── docs/                           # DATA_VALIDATION_REPORT.md
├── .cache/                         # Intermediate processing cache
└── README.md
```

## Rebuild the Mashup

```bash
python3 create_disaster_mashup.py
```

Sources are referenced relative to `../../`:
- `strange-places-mysterious-phenomena/individual/aviation_accidents.json` (NTSB)
- `strange-places-mysterious-phenomena/individual_complete/noaa_shipwrecks.json` (NOAA)
- `standalone-datasets/noaa-significant-storms/noaa_significant_storms.json` (NOAA)
- `standalone-datasets/usgs-significant-earthquakes/usgs_significant_earthquakes.json` (USGS)

All paths assume the script runs from this directory and `strange-places-mysterious-phenomena/` and `standalone-datasets/` are siblings in `~/datasets/`.

## Record Schema

Every record has: `category`, `latitude`, `longitude`, `name`, `date`, `subcategory`. Category-specific fields: `aircraft_type`/`event_id` (aviation), `magnitude`/`fatalities`/`injuries`/`damage`/`state` (storms), `depth_km` (earthquakes, but always null), `vessel_type` (shipwrecks, sparse).

## Known Quirks

- Aviation dates are year-only (`YYYY-01-01`), real dates are in event IDs
- Aviation records deduplicated on `event_id` (5,983 dupes removed)
- `depth_km` field exists but is always null
- Some coordinates are outside CONUS (Hawaii, Alaska, territories, international waters)

## Platforms

- **GitHub**: `lukeslp/us-disasters-mashup`
- **HuggingFace**: `lukeslp/us-disasters-mashup`
- **Kaggle**: `lucassteuber/us-disasters-mashup`
