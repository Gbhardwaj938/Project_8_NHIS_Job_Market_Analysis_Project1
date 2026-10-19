# Job Market Analysis and Recommendation System

## Project overview
Historical analysis of **244,828 Upwork job postings** from the supplied CSV. Includes data cleaning, keyword-based job categories, salary/budget analysis, monthly posting counts, country hourly-rate comparisons, a simple recommendation prototype, SQL examples, and Docker deployment files.

## Important limitations
- This is a historical snapshot, not a live job API. Observed posting dates span **2023-11-02 09:22:02** to **2024-03-24 14:16:47**.
- The source has only a short time window and monthly coverage is highly uneven. Long-term demand forecasts cannot be validated reliably from this file alone.
- Hourly rate currency is not explicitly identified in the supplied schema. Country rate comparisons are therefore numeric comparisons only, not verified FX-normalized salary comparisons.
- Remote work is inferred from words in the job title; this is an undercounting-prone proxy, not a definitive remote-work field.
- Categories are assigned using transparent title keywords. They are useful for an initial project but should be reviewed or improved with NLP/taxonomy.
- Upwork postings are freelance gigs, not a representative sample of all salaried jobs in each country.

## Folder structure
- `data/jobs_raw.csv`: supplied source snapshot
- `data/jobs_cleaned.csv`: parsed dates, midpoint rates, categories and remote keyword proxy
- `Job_Market_Analysis.ipynb`: end-to-end notebook
- `src/analysis.py`: reproducible analysis script
- `outputs/`: summary tables and JSON metrics
- `reports/`: charts and PDF report
- `app.py`, `templates/index.html`: Flask recommendation prototype
- `sql/schema_and_queries.sql`: MySQL schema and sample queries
- `Dockerfile`, `docker-compose.yml`: containerized web app
- `requirements.txt`: Python dependencies

## Run in VS Code (Windows)
1. Install Python 3.11 or 3.12 and the VS Code **Python** and **Jupyter** extensions.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   If Python 3.11 is not installed, install a supported Python version and update `py -3.11` accordingly.
5. Run analysis:
   ```powershell
   .\.venv\Scripts\python.exe src\analysis.py
   ```
6. Open `Job_Market_Analysis.ipynb`, select the `.venv` kernel, and run cells.
7. Launch the recommendation website:
   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

## Run with Docker
Install Docker Desktop, open a terminal in the project folder, then run:
```bash
docker compose up --build
```
Open `http://localhost:5000`. Stop with `Ctrl+C`; use `docker compose down` to remove the container.

## Recommendation API
`GET /api/recommend?query=python%20data&country=United%20States&hourly_only=true&limit=10`

Parameters:
- `query`: words to match in the job title
- `country`: optional country substring
- `hourly_only`: `true` / `false`
- `limit`: maximum 100

Response shape:
```json
{"count": 1, "recommendations": [{"title": "example", "country": "United States"}]}
```
`GET /health` returns a simple health check.

## Project tasks mapping
1. Title keywords and compensation: `outputs/title_keyword_salary_analysis.csv`
2. Emerging categories: `outputs/category_posting_counts.csv`; monthly trends in `outputs/monthly_trends.csv`
3. High-demand role forecasting: monthly series included; longer history is needed for a trustworthy forecast
4. Country hourly rate: `outputs/country_hourly_rates.csv` and chart
5. Recommendation engine: Flask title-keyword baseline and API
6. Monthly dynamics: `outputs/monthly_trends.csv` and charts
7. Remote landscape: title-keyword proxy in cleaned data
8. Future trends: report discusses limitations and the evidence needed for a defensible forecast

## Suggested future improvements
- Connect a permitted live job source/API and schedule refreshes.
- Collect at least 12–24 months of consistent history for time-series forecasts.
- Add currency metadata and convert rates to a common currency before country comparisons.
- Add skills/experience/location preferences and evaluate recommendations with Precision@K or NDCG.
- Add authentication, pagination, logging, tests and production WSGI server before public deployment.
