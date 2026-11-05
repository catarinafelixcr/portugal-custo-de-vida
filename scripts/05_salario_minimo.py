"""
National minimum wage (salário mínimo nacional), € per month, 14 payments a year.
Small fixed table from the legislation (also on PORDATA). Update once a year.
Output: data/clean/dim_salario_minimo.csv -> ano, salario_minimo
"""
import pandas as pd

from ine_api import save

SMN = {
    2015: 505, 2016: 530, 2017: 557, 2018: 580, 2019: 600, 2020: 635,
    2021: 665, 2022: 705, 2023: 760, 2024: 820, 2025: 870, 2026: 920,
}

df = pd.DataFrame(sorted(SMN.items()), columns=["ano", "salario_minimo"])
print(f"Minimum wage: {df.ano.min()}–{df.ano.max()}")
save(df, "dim_salario_minimo.csv")
