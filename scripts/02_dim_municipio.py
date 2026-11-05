"""
Municipality dimension: one row per municipality.

Built from the INE codes downloaded in 01_populacao.py, so no manual download is needed.
DICO = 2-digit district + 2-digit municipality (e.g. 0101 = Águeda, district 01 Aveiro).
Output: data/clean/dim_municipio.csv -> dico, municipio, cod_distrito, distrito, regiao
"""
import pandas as pd

from ine_api import CLEAN, DISTRITOS, save

nomes = pd.read_csv(CLEAN / "_nomes_municipios.csv", dtype={"dico": str})

# latest name for each code (names occasionally change spelling)
dim = (
    nomes.sort_values("ano")
         .groupby("dico", as_index=False)
         .last()[["dico", "municipio"]]
)
dim["cod_distrito"] = dim["dico"].str[:2]
dim["distrito"] = dim["cod_distrito"].map(DISTRITOS)
dim["regiao"] = dim["cod_distrito"].map(
    lambda c: "Madeira" if c.startswith("3") else "Açores" if c.startswith("4") else "Continente"
)

unknown = dim[dim["distrito"].isna()]
if not unknown.empty:
    print("  ⚠ codes without a district:", unknown["dico"].tolist())

print(f"Municipalities: {len(dim)} ({dim.regiao.value_counts().to_dict()})")
save(dim, "dim_municipio.csv")
