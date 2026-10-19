from pathlib import Path
from flask import Flask, render_template
import pandas as pd

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
GRAPH_DIR = ROOT / "static" / "graphs"
DATA_CANDIDATES = [
    ROOT / "data" / "jobs_cleaned.csv",
    ROOT / "jobs_cleaned.csv",
    ROOT / "data" / "job_postings.csv",
    ROOT / "job_postings.csv",
]

def load_jobs():
    for path in DATA_CANDIDATES:
        if path.exists():
            try:
                return pd.read_csv(path, low_memory=False), str(path.relative_to(ROOT))
            except Exception:
                pass
    return pd.DataFrame(), "Dataset not found"

def find_col(df, terms):
    for col in df.columns:
        if any(term in str(col).lower().strip() for term in terms):
            return col
    return None

@app.route("/")
def index():
    df, source = load_jobs()
    chart_defs = [
        ("Top job titles", "top_job_titles.png"),
        ("Salary distribution", "salary_distribution.png"),
        ("Posting trend", "posting_trend.png"),
        ("Top locations", "top_locations.png"),
        ("Work type distribution", "work_type_distribution.png"),
    ]
    charts = [{"title": title, "filename": filename} for title, filename in chart_defs if (GRAPH_DIR / filename).exists()]
    metrics = {
        "rows": f"{len(df):,}" if not df.empty else "—",
        "columns": str(len(df.columns)) if not df.empty else "—",
        "data_source": source,
    }
    top_titles = []
    if not df.empty:
        title_col = find_col(df, ["title", "job_title", "position"])
        if title_col:
            top_titles = df[title_col].dropna().astype(str).str.strip().value_counts().head(10).rename_axis("title").reset_index(name="postings").to_dict("records")
    return render_template("index.html", metrics=metrics, charts=charts, top_titles=top_titles)

if __name__ == "__main__":
    app.run(debug=True)
