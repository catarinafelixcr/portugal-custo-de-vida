# Is Portugal getting more expensive?

A Power BI project comparing how **population, salaries, house prices, fuel and food prices** have
evolved in Portugal, by municipality and district, using only free official open data.

> Status: 🚧 Phase 1 in progress — see [docs/PLAN.md](docs/PLAN.md)

## Questions

1. How has the population grown, and where?
2. Have salaries kept up with house prices, rents, fuel and food?
3. How many years of salary does it take to buy a home, by municipality?
4. How has the foreign resident population changed?

## Stack

- **Python** (pandas) — download and clean data from the INE API and other sources
- **Power BI Desktop** — data model (star schema), DAX measures, report
- **Git / GitHub** — version control (report saved as `.pbip` so changes are readable)

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python scripts/run_all.py        # downloads and cleans everything into data/clean/
```

Then open `powerbi/portugal.pbip` in Power BI Desktop and click **Refresh**.

## Project structure

```
scripts/      Python download + cleaning scripts (run_all.py runs them in order)
data/raw/     manual downloads (not versioned)
data/clean/   generated CSVs loaded by Power BI (not versioned)
powerbi/      Power BI project (.pbip)
docs/         plan, data sources, journal
```

## Data sources

All sources are public and free. Details, codes and caveats in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

- INE – Statistics Portugal (population, salaries, house prices, rents, CPI)
- DGEG and European Commission Weekly Oil Bulletin (fuel)
- AIMA / SEF (foreign residents)
- DGT – CAOP (municipal boundaries and codes)

## Screenshots

_Coming soon._
