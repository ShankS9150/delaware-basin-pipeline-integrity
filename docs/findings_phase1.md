# Phase 1 findings: reprojection validation

Validated NAD27 -> NAD83/UTM 13N conversion of 13,339 RRC surface wells
against RRC's own NAD83 coordinates (lat83/long83).

| Offset from RRC NAD83 | Wells | Median | Interpretation |
| --- | --- | --- | --- |
| Under 5 m | 12,609 (94.5%) | 0.1 m | Conversion correct |
| 5-100 m | 699 (5.2%) | ~46 m | Systematic: matches NAD27->NAD83 shift; likely stored in wrong datum |
| Over 100 m | 31 (0.2%) | 374 m | All reliability code 55; plotted location disagrees with recorded coordinates |

- 13,338 of 13,339 wells fall inside Reeves County.
- Setup note: NAD27 conversion requires the NOAA NADCON grid (us_noaa_conus.tif);
  without it PROJ silently returns infinite coordinates. ingest.py now fails loudly on this.
