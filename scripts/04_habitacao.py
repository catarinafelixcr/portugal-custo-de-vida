"""
Median sale price of dwellings (€/m², last 12 months) by municipality.

Source: INE 0012234 (NUTS 2024), quarterly from Q4 2019, all dwelling categories (total).
Each quarter already averages the previous 12 months, so Q4 of a year = that year's value.
Municipalities with fewer than 33 sales have no value (left blank on purpose).

Outputs:
  data/clean/fact_habitacao.csv            -> dico, ano, preco_m2           (annual = Q4)
  data/clean/fact_habitacao_trimestral.csv -> dico, ano, trimestre, preco_m2
"""
from ine_api import check, get_ine, keep_totals, only_municipalities, save

print("House prices (INE 0012234)…")
df = get_ine("0012234")          # all periods at once (Dim1=T)
df = only_municipalities(keep_totals(df)) if not df.empty else df

if not df.empty:
    df = (
        df.rename(columns={"valor": "preco_m2"})
          [["dico", "ano", "trimestre", "preco_m2"]]
          .dropna(subset=["preco_m2", "ano"])
          .drop_duplicates(["dico", "ano", "trimestre"])
          .sort_values(["dico", "ano", "trimestre"])
    )
    df["ano"] = df["ano"].astype(int)

check(df, "house prices", expected_municipalities=308)
save(df, "fact_habitacao_trimestral.csv")

# annual series: last available quarter of each year (Q4 when the year is complete)
annual = (
    df.sort_values("trimestre")
      .groupby(["dico", "ano"], as_index=False)
      .last()[["dico", "ano", "trimestre", "preco_m2"]]
      .rename(columns={"trimestre": "trimestre_ref"})
)
save(annual, "fact_habitacao.csv")
