"""
Resident population by municipality and year (31 December).

Source: INE 0012918 (NUTS 2024). Years missing there are taken from 0004167 (NUTS 2013).
The municipality code (DICO) is the same in both, so they combine cleanly.
Output: data/clean/fact_populacao.csv  ->  dico, ano, populacao
"""
from ine_api import annual_periods, check, get_ine, keep_totals, only_municipalities, save

FIRST, LAST = 2011, 2025
# Dim3 = sex, Dim4 = age group; 'T' = total
DIMS = {"Dim3": "T", "Dim4": "T"}


def fetch(varcd: str, years: range) -> "pd.DataFrame":
    df = get_ine(varcd, annual_periods(years.start, years.stop - 1), **DIMS)
    return only_municipalities(keep_totals(df)) if not df.empty else df


print("Population (INE 0012918, NUTS 2024)…")
pop = fetch("0012918", range(FIRST, LAST + 1))

have = set(pop["ano"].dropna().astype(int)) if not pop.empty else set()
missing = [y for y in range(FIRST, LAST + 1) if y not in have]
if missing:
    print(f"  years not in 0012918: {missing} -> trying 0004167 (NUTS 2013)…")
    old = fetch("0004167", range(min(missing), max(missing) + 1))
    if not old.empty:
        import pandas as pd
        pop = pd.concat([pop, old[old["ano"].isin(missing)]], ignore_index=True)

pop = (
    pop.rename(columns={"valor": "populacao", "geodsg": "municipio"})
       [["dico", "municipio", "ano", "populacao"]]
       .dropna(subset=["populacao"])
       .drop_duplicates(["dico", "ano"])
       .sort_values(["dico", "ano"])
)
pop["ano"] = pop["ano"].astype(int)
pop["populacao"] = pop["populacao"].astype(int)

check(pop, "population")
print(f"  Portugal {pop.ano.max()}: {pop[pop.ano == pop.ano.max()].populacao.sum():,} people")
save(pop[["dico", "ano", "populacao"]], "fact_populacao.csv")
# names are kept for building the municipality dimension
save(pop[["dico", "municipio", "ano"]], "_nomes_municipios.csv")
