# Deliverables by project task

| Task | Implemented artifact | Notes |
|---|---|---|
| 1. Title keywords vs compensation | `outputs/title_keyword_salary_analysis.csv`, `reports/keyword_hourly_rates.png` | Hourly rates and fixed budgets kept separate |
| 2. Emerging categories | `outputs/category_posting_counts.csv`, `reports/category_postings.png` | Categories are keyword heuristics; emerging growth needs longer history |
| 3. High-demand prediction | `outputs/monthly_trends.csv`, notebook trend section | Dataset window too short for validated future forecast |
| 4. Country hourly rates | `outputs/country_hourly_rates.csv`, `reports/country_hourly_rates.png` | Currency not explicitly identified |
| 5. Recommendation engine | `app.py`, `templates/index.html`, `API_DOCUMENTATION.md` | Keyword-ranked Flask prototype |
| 6. Monthly dynamics | `outputs/monthly_trends.csv`, `reports/monthly_postings.png` | Historical snapshot only |
| 7. Remote work trends | `remote_keyword` field in cleaned data and notebook | Title-keyword proxy only |
| 8. Future trends | PDF report and notebook caveats | Requires longer history for robust forecasting |
| Docker | `Dockerfile`, `docker-compose.yml` | Flask app exposed on port 5000 |
| SQL | `sql/schema_and_queries.sql` | MySQL schema and sample analytics queries |
