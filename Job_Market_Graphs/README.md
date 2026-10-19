# Job Market Analysis — Graphs and Dashboard

## Files
- `src/analysis_graphs.py`: creates charts from your CSV.
- `app.py`: Flask dashboard to display charts.
- `templates/index.html`: dashboard HTML.
- `static/graphs/`: generated PNG files.
- `requirements-graphs.txt`: required packages.

## Dataset location
Put your cleaned CSV at `data/jobs_cleaned.csv` (recommended) or `jobs_cleaned.csv` in this folder. It also checks `data/job_postings.csv` and `job_postings.csv`.

## Run in Windows / VS Code
```bash
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-graphs.txt
.\.venv\Scripts\python.exe src\analysis_graphs.py
.\.venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:5000

The script detects common column names for job title, salary, date, location and work type. If your CSV uses different column names, update the keyword lists in `src/analysis_graphs.py`.
