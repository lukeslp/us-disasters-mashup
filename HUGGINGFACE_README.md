---
license: cc0-1.0
task_categories:
  - feature-extraction
language:
  - en
tags:
  - disasters
  - aviation
  - shipwrecks
  - storms
  - earthquakes
  - geospatial
  - united-states
  - safety
  - natural-disasters
  - accidents
pretty_name: US Disasters Mashup
size_categories:
  - 10K<n<100K
---

# US Disasters Mashup

48,592 disasters: plane crashes, shipwrecks, severe storms, earthquakes

Unified dataset combining four major US disaster categories from government sources: NTSB aviation accidents, NOAA shipwrecks, NOAA severe storms, and USGS earthquakes. All data is public domain.

## Dataset Structure

[Check the demo notebook for data exploration examples]

## Usage

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("lukeslp/us-disasters-mashup")

# Or load from local files
import json
with open('data.json') as f:
    data = json.load(f)
```

## Citation

```bibtex
@dataset{us_disasters_mashup_2026,
  title = {US Disasters Mashup},
  author = {Steuber, Luke},
  year = {2026},
  url = {https://huggingface.co/datasets/lukeslp/us-disasters-mashup}
}
```

## Author

**Luke Steuber**
- Website: [lukesteuber.com](https://lukesteuber.com)
- Bluesky: [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)
- Email: luke@lukesteuber.com

## License

CC0-1.0
