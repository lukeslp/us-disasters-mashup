# Data Validation Report: US Disasters Mashup

**Validated**: 2026-02-14
**Dataset**: disasters_mashup.json (13 MB, 54,575 records)
**Verdict**: Authentic government data with known quality issues

## Summary

54,575 records from four US government sources, all verified as authentic. Category-specific fields are well-populated where they apply. Two significant quality issues: aviation dates are truncated to year-only precision, and ~5,983 duplicate aviation records exist.

## Dataset Composition

| Category | Records | % | Source |
|----------|---------|---|--------|
| Aviation Accidents | 32,410 | 59.4% | NTSB |
| Severe Storms | 14,770 | 27.1% | NOAA Storm Events |
| Earthquakes | 3,742 | 6.9% | USGS |
| Shipwrecks | 3,653 | 6.7% | NOAA AWOIS |

## Field Coverage

Fields are category-specific. Core fields (category, latitude, longitude, name, subcategory) are 100% populated across all records.

| Field | Coverage | Present In |
|-------|----------|-----------|
| category | 100% | All |
| latitude | 100% | All |
| longitude | 100% | All |
| name | 100% | All (e.g., "Tornado in OKLAHOMA, KIOWA") |
| subcategory | 100% | All (e.g., Tornado, Flash Flood, seismic, maritime, aviation) |
| date | 94.3% | All except some historical shipwrecks |
| aircraft_type | 59.4% | Aviation only (100% of aviation records) |
| event_id | 59.4% | Aviation only (NTSB event IDs) |
| magnitude | 19.9% | Storms (Fujita/EF scale) + Earthquakes (Richter) |
| fatalities | 27.1% | Storms only |
| injuries | 27.1% | Storms only |
| damage | 26.4% | Storms only (text: "250K", "1.5M") |
| state | 27.1% | Storms only |
| depth_km | 0% | Field exists but all values null |
| vessel_type | 0.6% | Shipwrecks, sparsely populated |
| cargo | <0.1% | Shipwrecks, almost empty |

## Coordinate Validation

- **100% populated**, zero missing
- Latitude range: -77.4 to 82.2
- Longitude range: -179.3 to 178.8
- Coordinate precision: 5-6 decimal places (meter-level, consistent with GPS/survey data)
- Round coordinates: <1% (rules out synthetic generation)
- ~3,200 records outside CONUS bounds: expected for Hawaii, Alaska, territories, international aviation/maritime

## Date Quality Issues

**Storms**: ISO 8601 dates with day precision (e.g., `1950-04-28`). Range: 1950-2025. Clean.

**Shipwrecks**: Mixed formats (`MM-DD-YYYY` or null). 85.8% missing dates. Historical records dating to the 1600s. Expected for archival maritime data.

**Aviation**: All 32,410 dates truncated to `YYYY-01-01`. The real dates appear embedded in the event IDs (e.g., event_id `20121010X84549` suggests Oct 10, 2012, but date field shows `2012-01-01`). This is a processing artifact, not fake data.

**Earthquakes**: Unix timestamps (e.g., `1766311037`). Consistent with USGS API output format. Not converted to ISO 8601.

## Duplicate Records

- 4,763 duplicate event IDs among aviation records
- 5,983 total extra records (some IDs appear 3+ times)
- Duplicates are exact copies (same coordinates, dates, all fields)
- Likely caused by overlapping source files during the original collection
- 18% duplication rate among records with event IDs

## Synthetic Data Check

No synthetic data indicators found:

- Record counts are non-round (32,410 / 14,770 / 3,742 / 3,653)
- Geographic distribution matches known patterns (tornado alley, Pacific seismic belt, coastal aviation corridors)
- Storm subcategories show realistic distribution (Tornado: 6,334; Flash Flood: 2,358; Thunderstorm Wind: 2,257)
- Earthquake magnitudes range 4.5-8.2 with realistic distribution
- NTSB event IDs follow the official NTSB Event ID format (YYYYMMDD + sequence)
- Storm damage values use NOAA's text format conventions ("250K", "1.5M")

## Storm Subcategory Breakdown

Top 10 storm types (from `subcategory` field):
1. Tornado: 6,334
2. Flash Flood: 2,358
3. Thunderstorm Wind: 2,257
4. Flood: 1,777
5. Hail: 1,246
6. Lightning: 574
7. Heavy Rain: 99
8. Marine Strong Wind: 43
9. Debris Flow: 43
10. Marine Thunderstorm Wind: 25

## Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| Aviation dates year-only | High | Real dates recoverable from event IDs |
| 5,983 duplicate records | Medium | Deduplication on event_id would fix |
| Earthquake dates as timestamps | Medium | Valid data, just not human-readable |
| depth_km always null | Low | Field exists but never populated |
| cargo/vessel_type sparse | Low | Most shipwreck records lack this detail |

## Overall Assessment

| Metric | Score |
|--------|-------|
| Source authenticity | 10/10 |
| Coordinate quality | 9/10 |
| Category-specific metadata | 8/10 |
| Date quality | 6/10 |
| Data cleanliness (duplicates) | 7/10 |
| Overall | 8/10 |

**Verdict**: Authentic data from four government APIs. Well-structured with category-specific fields (storms have casualties and damage, aviation has aircraft types and NTSB IDs, earthquakes have magnitude). Two improvement opportunities: deduplicate aviation records and recover full dates from event IDs.
