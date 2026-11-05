# Project plan — "Is Portugal getting more expensive?"

A step-by-step guide from an empty folder to a working Power BI report.
Tick the boxes as you go (`[ ]` → `[x]`) and commit this file, so Git keeps your progress too.

**Your setup:** Windows, VS Code, Python (via Anaconda). Everything below is free.

---

## Overview

| Phase | What | Result |
|---|---|---|
| 0 | Install tools, create folder, Git + GitHub | Empty project online |
| 1 | Population + salaries + house prices + minimum wage | First working report |
| 2 | Fuel prices | Fuel page + EU comparison |
| 3 | Food prices + foreign residents | Full cost-of-living story |
| 4 | Polish, README with screenshots, publish to GitHub | Portfolio project |

Rule of thumb: **finish each phase end-to-end (data → Power BI → commit) before starting the next.**

---

## Phase 0 — Setup (≈ 1 hour)

### Step 0.1 — Install the missing tools

- [ ] **Power BI Desktop** — Microsoft Store → search "Power BI Desktop" → Install.
      (The Store version updates itself automatically.)
- [ ] **Git** — download from <https://git-scm.com/download/win>, install with the default options.
      Check: open a new terminal and run `git --version`.
- [ ] **GitHub account** — sign up free at <https://github.com>.
- [ ] (Optional) **GitHub Desktop** — <https://desktop.github.com> if you prefer buttons to commands.
- [ ] **VS Code extensions** — open VS Code → Extensions (Ctrl+Shift+X) → install **Python** and **Jupyter** (Microsoft).

You already have Python (through Anaconda) and VS Code, so no separate Python install is needed.

### Step 0.2 — Configure Git (once per computer)

Open a terminal (in VS Code: **Ctrl+`**) and run, with your own name and the email of your GitHub account:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

### Step 0.3 — Put the project folder in place

1. Unzip `portugal-custo-de-vida.zip` into `C:\Users\<you>\Documents\`.
   Avoid OneDrive folders: syncing fights with Git and Power BI files.
2. You should see:

```
portugal-custo-de-vida/
├── README.md            ← project front page (GitHub shows this)
├── requirements.txt     ← Python packages
├── .gitignore           ← files Git must ignore
├── docs/
│   ├── PLAN.md          ← this file
│   ├── DATA_SOURCES.md  ← where every dataset comes from
│   └── JOURNAL.md       ← your notes: problems, decisions, ideas
├── scripts/             ← Python: download + clean
├── data/
│   ├── raw/             ← manual downloads (not in Git)
│   └── clean/           ← final CSVs for Power BI
└── powerbi/             ← the Power BI project
```

3. Open the folder in VS Code: **File → Open Folder…**

### Step 0.4 — Create the Python environment (venv)

A virtual environment is a private set of Python packages for this project only,
so nothing you install here can break your other projects.

In VS Code, open a terminal (**Ctrl+`**) and run:

```bash
cd %USERPROFILE%\Documents\portugal-custo-de-vida
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

- `python -m venv .venv` creates the `.venv` folder (Git ignores it).
- `.venv\Scripts\activate` turns it on: the prompt starts with `(.venv)`.
- `pip install …` installs pandas, requests, openpyxl and Jupyter support into it.

Then **Ctrl+Shift+P → Python: Select Interpreter →** choose the `.venv` one.
VS Code will now activate it automatically in new terminals for this folder.

> PowerShell says "running scripts is disabled"? Run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again.
> `python` not recognised? Run the `python -m venv .venv` line in **Anaconda Prompt** instead.

Every time you work on the project: `.venv\Scripts\activate`.

### Step 0.5 — Start Git and make the first commit

```bash
git init
git add .
git commit -m "Project structure and plan"
```

### Step 0.6 — Put it on GitHub

1. On github.com → **New repository** → name `portugal-custo-de-vida` →
   **don't** add a README or .gitignore (you already have them) → Create.
2. GitHub shows commands; run these (with your username):

```bash
git remote add origin https://github.com/<your-username>/portugal-custo-de-vida.git
git push -u origin main
```

A browser window asks you to sign in to GitHub the first time.

- [ ] Phase 0 done: the repo is visible on GitHub.

---

## Phase 1 — Population, salaries, house prices (≈ 1–2 weeks)

### Step 1.1 — Download and clean the data with Python

Everything in Phase 1 comes from the **INE API** (free, no account), so there are no manual downloads yet.

```bash
.venv\Scripts\activate
python scripts/run_all.py
```

This runs, in order:

| Script | Source | Output in `data/clean/` |
|---|---|---|
| `01_populacao.py` | INE 0012918 (+ 0004167 fallback) | `fact_populacao.csv` |
| `02_dim_municipio.py` | built from the INE geography codes | `dim_municipio.csv` |
| `03_salarios.py` | INE 0010385 (2015–2020) + 0012656 (2021+) | `fact_salarios.csv` |
| `04_habitacao.py` | INE 0012234 | `fact_habitacao.csv` |
| `05_salario_minimo.py` | fixed table (legislation) | `dim_salario_minimo.csv` |

- [ ] All 5 CSVs exist in `data/clean/`.
- [ ] Open each one in VS Code or Excel and check: 308 municipalities? sensible values? which years?
- [ ] Note anything strange in `docs/JOURNAL.md`.

If a script fails, read the message: most problems are a changed indicator code or a dimension
that isn't called "T". Paste the error to Claude and we fix it together.

```bash
git add scripts docs
git commit -m "Phase 1 data scripts working"
```

(The CSVs are generated, so they stay out of Git — anyone can recreate them with `run_all.py`.)

### Step 1.2 — Learn what you just downloaded (Python, optional but valuable)

Create `scripts/explore.ipynb` in VS Code and try:

```python
import pandas as pd
pop = pd.read_csv("../data/clean/fact_populacao.csv", dtype={"dico": str})
pop.groupby("ano")["populacao"].sum()          # Portugal total per year
pop[pop.ano == pop.ano.max()].nlargest(10, "populacao")   # biggest municipalities
```

### Step 1.3 — Create the Power BI project

1. Open Power BI Desktop.
2. **File → Options and settings → Options → Preview features** → tick
   **"Power BI Project (.pbip) save option"** (if it's there; in newer versions it's already on). Restart.
3. **File → Save as** → folder `powerbi/` → type **Power BI Project (*.pbip)** → name `portugal`.

> Why .pbip instead of .pbix? A .pbix is one binary blob, Git can't see what changed.
> A .pbip is a folder of text files (model, measures, pages), so Git shows your exact changes.

### Step 1.4 — Load the data

**Home → Get data → Text/CSV** → load each file from `data/clean/`.
For each one, click **Transform Data** before loading and check the column types:

- `dico` must be **Text** (otherwise "0101" becomes 101 and joins break)
- `ano` Whole number, values Decimal number

Then **Close & Apply**.

> Tip: In Power Query, create a parameter `PastaDados` with the path to `data/clean/` and use it
> in every source. If you move the project, you change one value instead of five.

### Step 1.5 — Build the data model (Model view, left sidebar)

Create a calendar table: **Modeling → New table**:

```DAX
dim_ano = 
DISTINCT (
    UNION (
        SELECTCOLUMNS ( fact_populacao, "ano", fact_populacao[ano] ),
        SELECTCOLUMNS ( fact_salarios, "ano", fact_salarios[ano] ),
        SELECTCOLUMNS ( fact_habitacao, "ano", fact_habitacao[ano] ),
        SELECTCOLUMNS ( dim_salario_minimo, "ano", dim_salario_minimo[ano] )
    )
)
```

Relationships (drag the column from one table onto the other), all **one-to-many, single direction**:

| From (one side) | To (many side) |
|---|---|
| `dim_municipio[dico]` | `fact_populacao[dico]` |
| `dim_municipio[dico]` | `fact_salarios[dico]` |
| `dim_municipio[dico]` | `fact_habitacao[dico]` |
| `dim_ano[ano]` | `fact_populacao[ano]` |
| `dim_ano[ano]` | `fact_salarios[ano]` |
| `dim_ano[ano]` | `fact_habitacao[ano]` |
| `dim_ano[ano]` | `dim_salario_minimo[ano]` |

This is a **star schema**: dimensions (who/where/when) in the middle, facts (numbers) around them.

- [ ] Model view shows the star, no many-to-many warnings.

### Step 1.6 — First DAX measures

Create a table to hold measures: **Home → Enter data** → name it `_Medidas` → Load.
Then select it and **New measure** for each:

```DAX
População = SUM ( fact_populacao[populacao] )

Ganho médio mensal = AVERAGE ( fact_salarios[ganho_medio_mensal] )

Preço mediano m2 = AVERAGE ( fact_habitacao[preco_m2] )

Salário mínimo = MAX ( dim_salario_minimo[salario_minimo] )

População var % =
VAR atual = [População]
VAR anterior = CALCULATE ( [População], dim_ano[ano] = MAX ( dim_ano[ano] ) - 1 )
RETURN DIVIDE ( atual - anterior, anterior )
```

> Note: averaging municipal salaries/prices is a simplification (a small municipality weighs
> the same as Lisbon). That's fine to start; improving it is a good Phase 4 exercise.

### Step 1.7 — The star chart: index base 100

```DAX
Ano base = 2019    -- (create as a measure; later replace with a slicer/parameter)

Índice preço casas =
VAR base = CALCULATE ( [Preço mediano m2], dim_ano[ano] = [Ano base] )
RETURN DIVIDE ( [Preço mediano m2], base ) * 100

Índice salário =
VAR base = CALCULATE ( [Ganho médio mensal], dim_ano[ano] = [Ano base] )
RETURN DIVIDE ( [Ganho médio mensal], base ) * 100

Índice salário mínimo =
VAR base = CALCULATE ( [Salário mínimo], dim_ano[ano] = [Ano base] )
RETURN DIVIDE ( [Salário mínimo], base ) * 100
```

2019 is the base because house price data starts at the end of 2019.

- [ ] Line chart: X = `dim_ano[ano]`, Y = the three indices. **This is the main story.**

### Step 1.8 — Report pages

- [ ] **Page 1 – Overview**: cards (population, average salary, price/m², minimum wage for the latest year) + the index chart.
- [ ] **Page 2 – Population**: line by year, bar by district, table of municipalities with growth %.
- [ ] **Page 3 – Housing vs salaries**: scatter (salary vs price/m² per municipality), "years of salary to buy 100 m²" measure.
- [ ] **Page 4 – My municipality**: one slicer, everything filters to it.
- [ ] Slicers for district and year on each page (use **View → Sync slicers**).

Useful extra measure:

```DAX
Anos de salário para 100m2 =
DIVIDE ( [Preço mediano m2] * 100, [Ganho médio mensal] * 14 )
```

(14 = salaries per year in Portugal, including holiday and Christmas pay.)

### Step 1.9 — Save, commit, push

```bash
git add .
git commit -m "Phase 1 report: population, salaries, housing"
git push
```

- [ ] Phase 1 done.

---

## Phase 2 — Fuel prices

### Step 2.1 — Manual downloads (save in `data/raw/combustiveis/`)

- [ ] **DGEG weekly prices since 2004** (XLS):
      <https://www.dgeg.gov.pt/pt/estatistica/energia/precos-de-energia/precos-de-combustiveis-em-portugal-continental/>
- [ ] **EU Weekly Oil Bulletin – "Price developments 2005 onwards"** (XLSX, ~4 MB):
      <https://energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en>

### Step 2.2 — Script `06_combustiveis.py` (we write it together when you get here)

- read the files with pandas, keep gasoline 95 and diesel
- convert €/1000 L → €/L (Oil Bulletin)
- average per year and month → `fact_combustiveis.csv` (national level, no `dico`)

### Step 2.3 — Power BI

- [ ] Relationship `dim_ano` → `fact_combustiveis`. **No** link to municipalities (national data).
- [ ] Add `Índice gasóleo` / `Índice gasolina` to the index chart.
- [ ] New page: Portugal vs EU, with and without taxes.
- [ ] Commit: `git commit -m "Phase 2: fuel prices"`

---

## Phase 3 — Food prices and foreign residents

### Step 3.1 — Food prices

- [ ] Script `07_ipc.py`: INE CPI, division 01 "Produtos alimentares e bebidas não alcoólicas" (monthly) → annual average → `fact_ipc.csv`.
      Also general CPI (all items), used to compute **real** values.
- [ ] Optional: small manual table `data/raw/cabaz_deco.csv` (date, value, link to the news article) for annotations.

### Step 3.2 — Foreign residents

- [ ] Script `08_estrangeiros.py`: INE 0013220 (by municipality, up to 2023).
- [ ] Manual: 2024 total and top nationalities from the AIMA *Relatório de Migrações e Asilo 2024* (PDF) → `data/raw/aima_2024.csv`.
- [ ] Show the SEF→AIMA series break clearly (different colour or a note), never as one continuous line.

### Step 3.3 — Power BI

- [ ] Real salary measure: `Ganho real = [Ganho médio mensal] / ([IPC] / 100)`.
- [ ] Page "Cost of living": food CPI vs salaries vs housing vs fuel indices.
- [ ] Page "Population & immigration".
- [ ] Commit.

---

## Phase 4 — Polish and publish

- [ ] **Maps**: TopoJSON of municipalities (from the DGT CAOP, simplified in <https://mapshaper.org>) + Shape Map visual, keyed by `dico`.
- [ ] Consistent theme (View → Themes → Customize) and titles that state the conclusion ("Houses rose X%, salaries Y%").
- [ ] Optional enrichment: mortgage rates (BPstat 12748390), unemployment (INE 0012136), local accommodation (RNAL), purchasing power by municipality.
- [ ] README: screenshots of each page, what you learned, how to run it.
- [ ] Export to PDF (File → Export → PDF) and add it to the repo, since the free version can't publish online.
- [ ] Final commit and push. Share the GitHub link on your CV/LinkedIn.

---

## Daily routine

```bash
cd %USERPROFILE%\Documents\portugal-custo-de-vida
.venv\Scripts\activate
git pull                          # if you work on more than one computer
# ... work ...
git status                        # what changed?
git add .
git commit -m "Short description of what you did"
git push
```

Good commit messages say *what* and *why*: `Fix dico as text in salaries`, not `changes`.

## Common problems

| Problem | Fix |
|---|---|
| `(.venv)` not shown in terminal | Run `.venv\Scripts\activate` (see step 0.4) |
| `git` not recognised | Close and reopen the terminal after installing Git |
| Script error "no data returned" | Indicator code or dimension changed; check the INE page of the indicator |
| Codes like 101 instead of 0101 | Column type must be Text in Power Query |
| Relationship is many-to-many | Duplicates in the dimension table; check `dim_municipio` |
| Index chart shows blanks | No data in the base year for that series; change `Ano base` |
