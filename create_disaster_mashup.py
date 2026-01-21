#!/usr/bin/env python3
"""
Disaster Mashup Dataset Creator

Combines multiple disaster data sources into a unified dataset:
- NTSB Aviation Accidents (32,410)
- NOAA Shipwrecks (3,653)
- NOAA Significant Storms (14,770)
- USGS Significant Earthquakes (3,742)

All sources are PUBLIC DOMAIN (US Government data).

Author: Luke Steuber
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent

# Data source paths
SOURCES = {
    'aviation_accidents': BASE_DIR / 'strange-places-mysterious-phenomena/individual/aviation_accidents.json',
    'shipwrecks': BASE_DIR / 'strange-places-mysterious-phenomena/individual_complete/noaa_shipwrecks.json',
    'storms': BASE_DIR / 'standalone-datasets/noaa-significant-storms/noaa_significant_storms.json',
    'earthquakes': BASE_DIR / 'standalone-datasets/usgs-significant-earthquakes/usgs_significant_earthquakes.json',
}

def normalize_record(record: dict, category: str) -> dict:
    """Normalize a record to the unified schema."""

    # Get latitude/longitude (different sources use different keys)
    lat = record.get('latitude') or record.get('lat')
    lon = record.get('longitude') or record.get('lon')

    # Convert to float if string
    try:
        lat = float(lat) if lat else None
        lon = float(lon) if lon else None
    except (ValueError, TypeError):
        lat = lon = None

    # Skip records without valid coordinates
    if lat is None or lon is None:
        return None

    # Get date
    date = record.get('date', '')
    if not date:
        year = record.get('year')
        if year and str(year) != '0':
            date = f"{year}-01-01"

    # Get name/title
    name = (record.get('name') or
            record.get('title') or
            record.get('location') or
            'Unknown')

    # Build normalized record
    normalized = {
        'category': category,
        'latitude': round(lat, 6),
        'longitude': round(lon, 6),
        'name': name[:200] if name else 'Unknown',
        'date': date[:10] if date else None,
    }

    # Add category-specific fields
    if category == 'aviation_accident':
        normalized['subcategory'] = 'aviation'
        normalized['aircraft_type'] = record.get('aircraft_make', '') + ' ' + record.get('aircraft_model', '')
        normalized['event_id'] = record.get('event_id')

    elif category == 'shipwreck':
        normalized['subcategory'] = 'maritime'
        normalized['vessel_type'] = record.get('vessel_type')
        normalized['cargo'] = record.get('cargo')

    elif category == 'storm':
        normalized['subcategory'] = record.get('event_type', 'storm')
        normalized['magnitude'] = record.get('magnitude')
        normalized['fatalities'] = record.get('fatalities')
        normalized['injuries'] = record.get('injuries')
        normalized['damage'] = record.get('damage_property')
        normalized['state'] = record.get('state')

    elif category == 'earthquake':
        normalized['subcategory'] = 'seismic'
        normalized['magnitude'] = record.get('magnitude')
        normalized['depth_km'] = record.get('depth')

    return normalized


def load_and_normalize(source_path: Path, category: str) -> list:
    """Load a source file and normalize all records."""
    if not source_path.exists():
        print(f"  Warning: {source_path} not found")
        return []

    with open(source_path) as f:
        data = json.load(f)

    records = []
    for record in data:
        normalized = normalize_record(record, category)
        if normalized:
            records.append(normalized)

    return records


def main():
    print("=" * 60)
    print("DISASTER MASHUP DATASET CREATOR")
    print("=" * 60)

    all_records = []

    # Load each source
    categories = {
        'aviation_accidents': 'aviation_accident',
        'shipwrecks': 'shipwreck',
        'storms': 'storm',
        'earthquakes': 'earthquake',
    }

    for source_key, category in categories.items():
        print(f"\nLoading {source_key}...")
        source_path = SOURCES[source_key]
        records = load_and_normalize(source_path, category)
        print(f"  Loaded {len(records):,} records")
        all_records.extend(records)

    print(f"\n{'='*60}")
    print(f"TOTAL RECORDS: {len(all_records):,}")

    # Count by category
    from collections import Counter
    cat_counts = Counter(r['category'] for r in all_records)
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count:,}")

    # Save output
    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / 'disasters_mashup.json'
    with open(output_path, 'w') as f:
        json.dump(all_records, f, indent=None, ensure_ascii=False)

    print(f"\nSaved to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Create metadata
    metadata = {
        'title': 'US Disasters Mashup',
        'description': 'Unified dataset of aviation accidents, shipwrecks, severe storms, and earthquakes',
        'record_count': len(all_records),
        'categories': dict(cat_counts),
        'sources': {
            'aviation_accidents': {
                'source': 'NTSB Aviation Accident Database',
                'url': 'https://www.ntsb.gov/safety/data',
                'license': 'Public Domain (US Government)'
            },
            'shipwrecks': {
                'source': 'NOAA AWOIS Database',
                'url': 'https://www.nauticalcharts.noaa.gov/data/wrecks-and-obstructions.html',
                'license': 'Public Domain (US Government)'
            },
            'storms': {
                'source': 'NOAA Storm Events Database',
                'url': 'https://www.ncdc.noaa.gov/stormevents/',
                'license': 'Public Domain (US Government)'
            },
            'earthquakes': {
                'source': 'USGS Earthquake Hazards Program',
                'url': 'https://earthquake.usgs.gov/',
                'license': 'Public Domain (US Government)'
            }
        },
        'created': datetime.now().isoformat(),
        'schema': {
            'category': 'Disaster type (aviation_accident, shipwreck, storm, earthquake)',
            'latitude': 'Decimal degrees (-90 to 90)',
            'longitude': 'Decimal degrees (-180 to 180)',
            'name': 'Event name or location',
            'date': 'Event date (YYYY-MM-DD)',
            'subcategory': 'Specific type within category',
            'magnitude': 'For earthquakes/storms: magnitude/intensity',
            'fatalities': 'Number of deaths (storms)',
            'injuries': 'Number of injuries (storms)'
        }
    }

    meta_path = output_dir / 'metadata.json'
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to: {meta_path}")


if __name__ == '__main__':
    main()
