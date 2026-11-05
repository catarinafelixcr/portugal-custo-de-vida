# Data sources

All free, no registration. INE data can be reused freely with the source cited.

## Phase 1

| Dataset | Source / code | Level | Frequency | Access | Notes |
|---|---|---|---|---|---|
| Resident population | INE **0012918** (NUTS 2024); old version **0004167** (NUTS 2013) | Municipality | Annual (31 Dec) | API | Revised after Census 2021 — always download the full series at once |
| Average monthly earnings | INE **0012656** (NUTS 2024, 2021+); **0010385** (NUTS 2013, older years) | Municipality (place of **work**) | Annual | API | Quadros de Pessoal: full-time private employees; ~15 months lag |
| Median sale price €/m² | INE **0012234** (NUTS 2024); **0011364** (NUTS 2013) | Municipality | Quarterly, rolling 12 months, from Q4 2019 | API | Blank where < 33 sales — leave blank, never 0 |
| National minimum wage | Legislation / PORDATA | National | Annual | Typed in script | 2026 = 920 € |

INE API pattern:

```
https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd=<code>&Dim1=<period>&lang=PT
https://www.ine.pt/ine/json_indicador/pindicaMeta.jsp?varcd=<code>&lang=PT     (metadata)
https://www.ine.pt/xurl/indx/<code>/PT                                          (web page, Excel export)
```

## Phase 2 — Fuel

| Dataset | Source | Level | Frequency | Link |
|---|---|---|---|---|
| Weekly fuel prices since 2004 | DGEG | Mainland | Weekly (Tuesdays 17h) | dgeg.gov.pt → Estatística → Preços de combustíveis em Portugal Continental |
| Daily average price | DGEG | Mainland | Daily, CSV export | precoscombustiveis.dgeg.gov.pt/estatistica/preco-medio-diario/ |
| EU Weekly Oil Bulletin | European Commission | Country (EU-27) | Weekly since 2005 | energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en |

No official history per fuel station exists; district-level history requires collecting it yourself daily.

## Phase 3 — Food and foreign residents

| Dataset | Source | Level | Notes |
|---|---|---|---|
| CPI – food and non-alcoholic beverages (COICOP 01) | INE (monthly); Eurostat `prc_hicp_midx` CP01 | National / NUTS II | Main series. INE moved to CPI base 2025 — rebase to your base year |
| DECO PROteste basket (63 products) | Press releases only | National | Context only, not downloadable. Started 5 Jan 2022 |
| Foreign residents | INE **0013220** | Municipality | Up to 2023 |
| Foreign residents 2024 | AIMA, *Relatório de Migrações e Asilo 2024* (PDF) | District | **Series break**: AIMA revised 2023 from 1,044,606 to 1,304,833 |

## Enrichment (optional)

| Dataset | Source | Why |
|---|---|---|
| General CPI / HICP | INE, Eurostat | Real (inflation-adjusted) salaries and prices |
| Mortgage interest rate | BPstat series 12748390 | Cost of paying for the house, not just its price |
| Unemployment rate | INE 0012136 (NUTS II, quarterly) | Labour-market context |
| Purchasing power by municipality | INE *Estudo sobre o Poder de Compra Concelhio* | Effective income by municipality |
| Local accommodation (Alojamento Local) | Turismo de Portugal RNAL (travelBI open data) | Tourism pressure on housing |
| Rents €/m² of new contracts | INE (search "valor mediano das rendas", NUTS 2024) | Rental market, from 2017 |

## Maps and codes

| Need | Source |
|---|---|
| Official municipality codes (DICO = district 2 digits + municipality 2 digits) | INE geography codes (last 4 characters of a municipality `geocod`); DGT CAOP |
| Boundaries | DGT **CAOP** (GeoPackage/Shapefile, CC BY 4.0): dgterritorio.gov.pt → Cartografia → CAOP |
| TopoJSON for Power BI Shape Map | Convert CAOP in mapshaper.org (simplify ~5–10%, export TopoJSON), or GitHub `deldersveld/topojson` (districts) |

## Pitfalls when combining

1. Join on **codes**, never names (Calheta and Lagoa exist twice). Keep codes as **text**.
2. Districts ≠ NUTS regions. Aggregate municipality → district, never NUTS → district.
3. NUTS 2013 vs 2024 have different region codes, but the municipality code (DICO) is the same.
4. Series breaks: housing "Metodologia 2022", CPI base change, population revisions, SEF → AIMA.
5. Different frequencies: convert to annual averages before computing indices.
6. Different last years: salaries end earlier than prices — compare up to the last common year.
7. Always show nominal **and** real values.
