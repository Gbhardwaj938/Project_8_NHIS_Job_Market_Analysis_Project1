from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_CANDIDATES = [
    ROOT / "data" / "jobs_cleaned.csv",
    ROOT / "jobs_cleaned.csv",
    ROOT / "data" / "job_postings.csv",
    ROOT / "job_postings.csv",
]
OUT = ROOT / "static" / "graphs"
OUT.mkdir(parents=True, exist_ok=True)

def find_data():
    for path in DATA_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("CSV not found. Put jobs_cleaned.csv in data/ or project root.")

def find_column(df, keywords):
    for col in df.columns:
        if any(word in str(col).lower().strip() for word in keywords):
            return col
    return None

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)

def main():
    path = find_data()
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]

    title_col = find_column(df, ["title", "job_title", "position"])
    if title_col:
        values = df[title_col].dropna().astype(str).str.strip().value_counts().head(12)
        if not values.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            values.sort_values().plot(kind="barh", ax=ax)
            ax.set(title="Top 12 Job Titles by Posting Count", xlabel="Number of postings", ylabel="Job title")
            save(fig, "top_job_titles.png")

    salary_col = find_column(df, ["salary", "pay", "compensation", "annual_income"])
    if salary_col:
        values = pd.to_numeric(df[salary_col].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce").dropna()
        values = values[values > 0]
        if len(values) >= 2:
            values = values[values <= values.quantile(.99)]
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.hist(values, bins=30)
            ax.set(title="Salary Distribution (numeric values only)", xlabel=f"Salary field: {salary_col}", ylabel="Number of postings")
            save(fig, "salary_distribution.png")

    date_col = find_column(df, ["date_posted", "posted_date", "posting_date", "created_at", "date"])
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
        if not dates.empty:
            trend = dates.dt.to_period("M").value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(trend.index.astype(str), trend.values, marker="o")
            ax.set(title="Job Posting Trend by Month", xlabel="Month", ylabel="Number of postings")
            ax.tick_params(axis="x", rotation=45)
            save(fig, "posting_trend.png")

    location_col = find_column(df, ["country", "location", "job_location"])
    if location_col:
        values = df[location_col].dropna().astype(str).str.strip().value_counts().head(10)
        if not values.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            values.sort_values().plot(kind="barh", ax=ax)
            ax.set(title="Top 10 Job Locations", xlabel="Number of postings", ylabel="Location")
            save(fig, "top_locations.png")

    work_col = find_column(df, ["remote", "work_type", "workplace", "employment_type", "job_type"])
    if work_col:
        values = df[work_col].dropna().astype(str).str.strip().value_counts().head(10)
        if not values.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            values.plot(kind="bar", ax=ax)
            ax.set(title="Work Type / Remote Category Distribution", xlabel="Category", ylabel="Number of postings")
            ax.tick_params(axis="x", rotation=35)
            save(fig, "work_type_distribution.png")

    print(f"Dataset: {path}")
    print(f"Rows: {len(df):,}; columns: {len(df.columns)}")
    print(f"Charts saved in: {OUT}")
    print("Only charts supported by detected CSV columns are generated.")

if __name__ == "__main__":
    main()
