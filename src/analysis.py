from pathlib import Path
import pandas as pd
import numpy as np
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "jobs_raw.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

CATEGORY_RULES = {
    "Software & Web Development": ["developer","development","programming","software","website","web app","wordpress","shopify","react","python","javascript","php","api","full stack","frontend","backend","mobile app","flutter","android","ios"],
    "Data & Analytics": ["data analyst","data analysis","data science","machine learning","artificial intelligence"," ai ","analytics","sql","power bi","tableau","excel","dashboard","forecast","statistical","deep learning"],
    "Design & Creative": ["designer","design","graphic","logo","figma","ui/ux","ux ","illustration","video editing","animation","photoshop","branding"],
    "Writing & Translation": ["writer","writing","copywriting","content","proofread","translation","translator","blog","seo article"],
    "Marketing & Sales": ["marketing","seo","social media","media buyer","facebook ads","google ads","lead generation","sales","email campaign","advertising","smma","growth"],
    "Admin & Customer Support": ["virtual assistant","customer support","customer service","data entry","administrative","appointment setter","chat support","transcription"],
    "Finance & Accounting": ["accountant","bookkeeping","finance","financial","quickbooks","tax","payroll"],
    "Engineering & Architecture": ["engineer","engineering","cad","autocad","architecture","architect","3d modeling","solidworks"],
}
def classify(title):
    t = " " + str(title).lower() + " "
    for category, keywords in CATEGORY_RULES.items():
        if any(word in t for word in keywords):
            return category
    return "Other"

def main():
    df = pd.read_csv(DATA)
    df["published_date"] = pd.to_datetime(df["published_date"], utc=True, errors="coerce")
    df["date"] = df["published_date"].dt.tz_convert(None)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df["country"] = df["country"].fillna("Unknown").replace("", "Unknown")
    df["is_hourly"] = df["is_hourly"].fillna(False).astype(bool)
    df["hourly_mid"] = df[["hourly_low","hourly_high"]].mean(axis=1, skipna=True)
    df["category"] = df["title"].map(classify)
    df["remote_keyword"] = df["title"].str.lower().str.contains(r"\b(remote|work from home|wfh|anywhere|virtual)\b", regex=True, na=False)
    df.to_csv(OUT / "jobs_cleaned.csv", index=False)
    df.groupby("month").agg(postings=("title","size"), hourly_postings=("is_hourly","sum")).reset_index().to_csv(OUT/"monthly_trends.csv",index=False)
    df["category"].value_counts().rename_axis("category").reset_index(name="posting_count").to_csv(OUT/"category_posting_counts.csv",index=False)
    df[df["is_hourly"] & df["hourly_mid"].notna() & df["country"].ne("Unknown")].groupby("country").agg(
        job_count=("title","size"), avg_hourly_rate=("hourly_mid","mean"), median_hourly_rate=("hourly_mid","median")
    ).query("job_count >= 30").sort_values("job_count",ascending=False).to_csv(OUT/"country_hourly_rates.csv")
    print(f"Analysis complete: {len(df):,} rows. Outputs saved in {OUT}")
if __name__ == "__main__":
    main()
