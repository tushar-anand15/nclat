# NCLAT Scraper

A web scraper for the **National Company Law Appellate Tribunal (NCLAT)** website. It collects case data and orders across NCLAT benches for a given date range and location, so the data can be structured and analysed instead of browsed one page at a time.

## What it does

- Navigates the NCLAT judgments portal by date range and bench location (e.g. New Delhi, Chennai).
- Builds the case list for the period, then processes each case to extract details and download orders.
- Uses Selenium to drive the site and logs each run for reproducibility.

## Requirements

- Python 3.7+
- Selenium + a matching ChromeDriver
- See imports in `SRC/` for the full dependency list

## Usage

Set the date range and locations at the top of `SRC/main.py`:

```python
FROM_DATE = '07/01/2024'   # MM/DD/YYYY
TO_DATE   = '07/10/2024'
LOCATIONS = ['New Delhi', 'Chennai']
```

Then run:

```bash
cd SRC
python main.py
```

Output (HTML, parsed data, downloaded orders, logs) is written to the run's data directories.

## Layout

```
SRC/
├── main.py        # entry point — date range + locations
├── nav.py         # site navigation (Selenium)
├── util_funcs.py  # case list, per-case processing, drivers, logging
└── consts.py      # constants
```
