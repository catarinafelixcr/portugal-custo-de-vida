"""
Average monthly earnings (ganho médio mensal, €) by municipality and year.

Source: INE, Quadros de Pessoal (full-time private-sector employees; geography = place of WORK).
  - 0010385 (NUTS 2013) for 2015–2020
  - 0012656 (NUTS 2024) for 2021 onwards
Output: data/clean/fact_salarios.csv -> dico, ano, ganho_medio_mensal
"""
import pandas as pd

from ine_api import annual_periods, check, get_ine, keep_totals, only_municipalities, save

FIRST_OLD, LAST_OLD = 2015, 2020
FIRST_NEW, LAST_NEW = 2021, 2025  # future years simply return nothing

print("Salaries 2021+ (INE 0012656)…")
new = get_ine("0012656", annual_periods(FIRST_NEW, LAST_NEW))
print("Salaries 2015–2020 (INE 0010385)…")
old = get_ine("0010385", annual_periods(FIRST_OLD, LAST_OLD))

frames = [only_municipalities(keep_totals(d)) for d in (new, old) if not d.empty]
sal = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

if not sal.empty:
    sal = (
        sal.rename(columns={"valor": "ganho_medio_mensal"})
           [["dico", "ano", "ganho_medio_mensal"]]
           .dropna()
           .drop_duplicates(["dico", "ano"])   # if a year is in both, keep the NUTS 2024 one
           .sort_values(["dico", "ano"])
    )
    sal["ano"] = sal["ano"].astype(int)
    sal["ganho_medio_mensal"] = sal["ganho_medio_mensal"].round(2)

check(sal, "salaries")
save(sal, "fact_salarios.csv")
