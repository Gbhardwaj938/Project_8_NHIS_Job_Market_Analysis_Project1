# API Documentation

Base URL (local): `http://127.0.0.1:5000`

## GET /api/recommend
Query parameters:
- `query` (string, optional): title keywords, e.g. `python data`
- `country` (string, optional): substring filter, e.g. `India`
- `hourly_only` (boolean string, optional): `true` or `false`
- `limit` (integer, optional): defaults to 20; capped at 100

Example:
`GET /api/recommend?query=python%20data&country=India&hourly_only=true&limit=10`

Returns JSON with `count` and `recommendations`. Each result can include title, country, category, hourly/fixed compensation fields, date and original posting URL.

## GET /health
Returns `{"status":"ok"}` when the Flask process is running.

## Ranking method
Each whitespace-separated query term found in a title adds one point. Results are sorted by score descending, then date descending. This is a transparent baseline; it is not a trained machine-learning model.
