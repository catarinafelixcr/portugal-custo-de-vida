"""
Small helper for the INE (Statistics Portugal) JSON API.

Free, no account needed. Docs:
https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api

Main function: get_ine(varcd, periods, **dims) -> tidy pandas DataFrame with columns
    periodo, ano, trimestre, geocod, geodsg, <dim_N, dim_N_t ...>, valor
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
META = "https://www.ine.pt/ine/json_indicador/pindicaMeta.jsp"

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
RAW = ROOT / "data" / "raw"
CLEAN.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

DISTRITOS = {
    "01": "Aveiro", "02": "Beja", "03": "Braga", "04": "Bragança",
    "05": "Castelo Branco", "06": "Coimbra", "07": "Évora", "08": "Faro",
    "09": "Guarda", "10": "Leiria", "11": "Lisboa", "12": "Portalegre",
    "13": "Porto", "14": "Santarém", "15": "Setúbal", "16": "Viana do Castelo",
    "17": "Vila Real", "18": "Viseu",
    # Autonomous regions: DICO starts with 3x (Madeira) or 4x (Azores islands)
    "31": "R. A. Madeira", "32": "R. A. Madeira",
    **{f"4{i}": "R. A. Açores" for i in range(1, 10)},
}

_session = requests.Session()
_session.headers["User-Agent"] = "portugal-custo-de-vida (learning project)"


def _request(url: str, params: dict, retries: int = 3) -> list | dict:
    for attempt in range(1, retries + 1):
        try:
            r = _session.get(url, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            if attempt == retries:
                raise RuntimeError(f"INE API failed for {params}: {e}") from e
            time.sleep(2 * attempt)


def metadata(varcd: str) -> dict:
    """Indicator metadata (name, dimensions, unit). Useful when exploring a new code."""
    data = _request(META, {"varcd": varcd, "lang": "PT"})
    return data[0] if isinstance(data, list) else data


def _to_number(x):
    """INE values are strings; symbols like 'x', '//', '…' mean 'not available'."""
    if x is None:
        return None
    s = str(x).strip().replace(" ", "")
    if not s or not re.fullmatch(r"-?\d+([.,]\d+)?", s):
        return None
    return float(s.replace(",", "."))


def _parse_period(label: str) -> tuple[int | None, int | None]:
    """'2023' -> (2023, None); '4.º Trimestre de 2019' / '2019T4' -> (2019, 4)."""
    year = re.search(r"(19|20)\d{2}", label)
    year = int(year.group()) if year else None
    q = re.search(r"(\d)\s*\.?\s*º?\s*[Tt]rimestre", label) or re.search(r"[Tt]\s*(\d)\b", label)
    return year, (int(q.group(1)) if q else None)


def parse_response(data) -> pd.DataFrame:
    """Turn one API response into a tidy DataFrame."""
    block = data[0] if isinstance(data, list) else data
    if str(block.get("Sucesso", {})).lower().find("falso") >= 0:
        return pd.DataFrame()
    dados = block.get("Dados") or {}
    rows = []
    for periodo, registos in dados.items():
        ano, trimestre = _parse_period(periodo)
        for reg in registos:
            row = {"periodo": periodo, "ano": ano, "trimestre": trimestre}
            row.update({k: v for k, v in reg.items() if k != "valor"})
            row["valor"] = _to_number(reg.get("valor"))
            rows.append(row)
    return pd.DataFrame(rows)


def get_ine(varcd: str, periods: list[str] | None = None, **dims) -> pd.DataFrame:
    """
    Download an indicator.

    periods: list of INE period codes, e.g. ['S7A2015', 'S7A2016'] for annual data.
             None -> all periods (Dim1=T). Large indicators may need per-year calls.
    dims:    other dimensions, e.g. Dim3='T' (total) — see metadata(varcd).
    """
    frames = []
    for p in periods or ["T"]:
        params = {"op": "2", "varcd": varcd, "Dim1": p, "lang": "PT", **dims}
        df = parse_response(_request(BASE, params))
        if not df.empty:
            frames.append(df)
        time.sleep(0.3)  # be polite to the server
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def annual_periods(first: int, last: int) -> list[str]:
    return [f"S7A{y}" for y in range(first, last + 1)]


def keep_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    For every extra dimension (dim_3, dim_4 ...), keep only the 'Total' category,
    if there is one. Leaves the geography untouched.
    """
    for col in [c for c in df.columns if re.fullmatch(r"dim_\d+", c)]:
        codes = df[col].astype(str)
        if (codes == "T").any():
            df = df[codes == "T"]
        elif f"{col}_t" in df and df[f"{col}_t"].str.lower().eq("total").any():
            df = df[df[f"{col}_t"].str.lower() == "total"]
    return df


def only_municipalities(df: pd.DataFrame) -> pd.DataFrame:
    """
    INE municipality geocod = NUTS III code (3 chars) + DICO (4 digits), e.g. '1111601'.
    Keeps those rows and adds 'dico' (as text, keeps the leading zero).
    """
    g = df["geocod"].astype(str).str.strip()
    mask = (g.str.len() == 7) & g.str[-4:].str.isdigit()
    out = df[mask].copy()
    out["dico"] = g[mask].str[-4:]
    return out


def save(df: pd.DataFrame, name: str) -> Path:
    path = CLEAN / name
    df.to_csv(path, index=False, encoding="utf-8-sig")  # utf-8-sig: Excel/Power BI read accents correctly
    print(f"  saved {path.relative_to(ROOT)}  ({len(df):,} rows)")
    return path


def check(df: pd.DataFrame, what: str, expected_municipalities: int = 308) -> None:
    """Quick sanity report printed after each script."""
    if df.empty:
        raise SystemExit(f"  !! {what}: no data returned. Check the indicator code/dimensions on the INE site.")
    n = df["dico"].nunique() if "dico" in df else None
    years = sorted(df["ano"].dropna().unique().astype(int)) if "ano" in df else []
    print(f"  {what}: years {years[0]}–{years[-1]}, municipalities {n}")
    if n is not None and n != expected_municipalities:
        print(f"  ⚠ expected {expected_municipalities} municipalities, got {n} — have a look.")
