from pathlib import Path
import pandas as pd
from flask import Flask, request, render_template, jsonify

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "jobs_cleaned.csv"
app = Flask(__name__)

def load_jobs():
    df = pd.read_csv(DATA)
    for col in ["title","country","category"]:
        if col in df: df[col] = df[col].fillna("")
    return df

def recommend_jobs(query="", country="", hourly_only=False, limit=20):
    df = load_jobs()
    query = query.strip().lower()
    if country:
        df = df[df["country"].str.lower().str.contains(country.lower(), na=False)]
    if hourly_only:
        df = df[df["is_hourly"].astype(str).str.lower().isin(["true","1"])]
    if query:
        terms = [t for t in query.split() if t]
        df["_score"] = df["title"].str.lower().apply(lambda title: sum(1 for t in terms if t in title))
        df = df[df["_score"] > 0].sort_values(["_score","date"], ascending=[False,False])
    else:
        df = df.sort_values("date", ascending=False)
    cols = [c for c in ["title","country","category","is_hourly","hourly_low","hourly_high","budget","date","link"] if c in df.columns]
    return df[cols].head(max(1,min(int(limit),100))).replace({float("nan"):None}).to_dict(orient="records")

@app.route("/", methods=["GET","POST"])
def home():
    query = request.values.get("query","")
    country = request.values.get("country","")
    hourly_only = request.values.get("hourly_only") == "on"
    jobs = recommend_jobs(query,country,hourly_only,30)
    return render_template("index.html", jobs=jobs, query=query, country=country, hourly_only=hourly_only)

@app.route("/api/recommend", methods=["GET"])
def api_recommend():
    jobs = recommend_jobs(
        request.args.get("query",""),
        request.args.get("country",""),
        request.args.get("hourly_only","false").lower() in ["true","1","yes"],
        request.args.get("limit",20)
    )
    return jsonify({"count":len(jobs),"recommendations":jobs})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
