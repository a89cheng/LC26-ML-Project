# Launch Window Dashboard — Full Project Context

This document contains everything needed to continue working on this project in any new conversation. Paste it at the start of a new chat with the instruction: _"Read this document and help me continue building this project."_

---

## Who I Am

- Student at University of Waterloo, member of Waterloo Rocketry
- Background: Python, HTML, CSS — limited JS experience
- Goal: data engineering / software engineering roles
- Timeline: 65 days to ship the full project

---

## What This Project Is

A **real-time launch window prediction dashboard** for the Waterloo Rocketry team. It answers one question: _given the weather forecast for the next 24 hours, which hours are safe to launch?_

The system:
1. Fetches hourly weather forecasts from Open-Meteo (free, no API key) for the Launch Canada site near Sudbury, Ontario
2. Runs the forecast through a rocket landing dispersion model (existing Python code)
3. Runs an ML classifier to output P(safe launch) for each hour
4. Stores results in a PostgreSQL database
5. Displays a live-updating React dashboard

This project demonstrates: ETL pipeline, time-series database, REST API, ML model serving, real-time React frontend — end to end.

---

## Launch Site

```
Latitude:  47.965378°N
Longitude: -81.873536°W
Location:  Near Sudbury, Ontario (Launch Canada advanced pad)
Safe zone: 10 nautical miles (18,520 m) radius
```

---

## Existing Codebase

Three Python modules already exist and are **not to be rewritten** — they are the computation engine:

### `dispersion_backend.py`
Core math and plotting. Key functions:
- `ellipse_math(x, y)` — eigendecomposition of covariance matrix, returns ellipse center, eigenvalues, rotation angle
- `haversine_nm(ref_lat, ref_lon, lat, lon)` — great-circle distance in nautical miles
- `get_outliers(radius_nm, ref_lat, ref_lon, lat, lon)` — indices of points outside radius
- `plot_data(...)` — plots CSV data onto matplotlib axes
- `save_plot(...)` — saves 300 DPI PNG
- `_extract_columns(data)` — handles both "Polaris" and "Aurora" CSV naming conventions
- `_finish_axes(...)` — applies legend, labels, LC ellipse, known locations to axes
- `_plot_file(...)` — plots a single CSV file's rocket and payload scatter points

### `statistics_backend.py`
Outlier analysis and flight stats. Key functions:
- `coordinate_stats(historical_file_path)` → returns `RocketStats` object with 10 statistics
- `get_outlier_indices(historical_file)` → row indices of flights outside 10 NM
- `store_launch_information(outlier_indices, sim_params_file, historical_file)` → list of `Outlying_Launch` objects with full wind profiles at 19 altitudes
- `sort_outliers_winds(launch_data)` → sorted by max and average wind speed
- `plotting_top_outliers(...)` → wind speed vs altitude chart with quiver arrows

### `dispersion_app.py`
The old Tkinter GUI — **being replaced entirely** by the React frontend. Logic has been extracted to the two backend modules. Do not add features to this file.

---

## RocketStats Fields

```python
total_simulations       # row count
mean_apogee             # mean of Apogee (ft)
std_apogee              # std of Apogee (ft)
mean_landing_distance   # mean distance in miles (Euclidean — known issue)
std_landing_distance
max_landing_distance
accuracy_launches       # fraction within 10 NM
mean_min_stability      # mean of Min Stability column
mean_lateral_velocity   # mean lateral velocity at apogee (m/s)
mean_wind_speed         # mean of Max Windspeed (mph)
```

---

## CSV Column Names

Two naming conventions exist. `_get_col()` handles both:

| Data | Polaris column | Aurora column |
|---|---|---|
| Rocket lat | `Polaris Rocket Landing Latitude (°N)` | `Aurora Rocket Landing Latitude (°N)` |
| Rocket lon | `Polaris Rocket Landing Longitude (°E)` | `Aurora Rocket Landing Longitude (°E)` |
| Payload lat | `Polaris Deployable Payload Landing Latitude (°N)` | `Deployable Payload Landing Latitude (°N)` |
| Payload lon | `Polaris Deployable Payload Landing Longitude (°E)` | `Deployable Payload Landing Longitude (°E)` |

Other columns (Polaris naming, hardcoded in statistics_backend):
```
Apogee (ft)
Max Windspeed (mph)
Wind Direction (deg)
Polaris Rocket Position East of Launch (ft)
Polaris Rocket Position North of Launch (ft)
Polaris Rocket Min Stability
Polaris Rocket Lateral Velocity at Apogee (m/s)
```

Simulation parameters CSV (wind profiling) uses altitude as column name:
```
110, 320, 500, 800, 1000, 1500, 1900, 3200, 4200, 5600,
7200, 9200, 10400, 11800, 13500, 15800, 17700, 19300, 22000
direction [110], direction [320], ... direction [22000]
```

---

## Known Bugs in Existing Code (do not fix until v2)

1. `coordinate_stats()` uses Euclidean distance in feet for landing distance — inconsistent with `haversine_nm` used elsewhere
2. `get_outlier_indices()` hardcodes Polaris column names — will fail on Aurora exports
3. `plot_known_locations()` hardcodes Highway 144 CSV path as `../Road Coordinates/highway_144.csv`
4. Launch lat/lon hardcoded in multiple places — should be a single config constant
5. `plotting_top_outliers` guard `if ax1 is None` at bottom is always False when called from app

---

## Full Tech Stack

```
Backend:
  FastAPI          — REST API, Python
  APScheduler      — hourly pipeline job
  SQLAlchemy       — ORM, DB connection
  PostgreSQL        — database (TimescaleDB extension optional)
  httpx            — async HTTP client for Open-Meteo
  XGBoost          — ML classifier
  scikit-learn     — feature engineering, model evaluation
  joblib           — model serialization
  pandas / numpy / scipy — existing math dependencies

Frontend:
  React (Vite)     — UI framework
  Tailwind CSS     — styling
  react-leaflet    — interactive map
  Chart.js         — wind altitude chart
  react-chartjs-2  — React wrapper
  Recharts         — historical time series chart

Infrastructure:
  Docker / docker-compose — runs PostgreSQL locally
  Open-Meteo       — free weather forecast API, no key needed
```

---

## Project Folder Structure

```
launch-window/
│
├── backend/
│   ├── main.py                    ← FastAPI app, all routes
│   ├── pipeline.py                ← APScheduler, hourly job orchestration
│   ├── weather.py                 ← Open-Meteo API client + parser
│   ├── predict.py                 ← dispersion math + ML inference
│   ├── database.py                ← SQLAlchemy models + DB helpers
│   ├── ml/
│   │   ├── train.py               ← XGBoost training script
│   │   ├── features.py            ← feature engineering from forecast dict
│   │   └── model.joblib           ← saved trained model
│   ├── core/
│   │   ├── dispersion_backend.py  ← existing code, unchanged
│   │   └── statistics_backend.py  ← existing code, unchanged
│   └── data/
│       └── highway_144.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── MapPanel.jsx           ← react-leaflet, landing ellipse
│   │   │   ├── TimelineBar.jsx        ← 24hr GO/NO-GO hour slots
│   │   │   ├── ForecastCard.jsx       ← detail for selected hour
│   │   │   ├── WindProfileChart.jsx   ← Chart.js altitude chart
│   │   │   ├── SafetyGauge.jsx        ← P(safe) display, GO/NO-GO label
│   │   │   ├── FeatureImportance.jsx  ← top risk altitudes
│   │   │   └── HistoryChart.jsx       ← Recharts 30-day time series
│   │   ├── hooks/
│   │   │   ├── usePredictions.js      ← fetches + auto-refreshes every 15min
│   │   │   └── useWeather.js          ← current forecast for display
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── notebooks/
│   └── ml_exploration.ipynb       ← EDA, training, feature importance
│
├── scripts/
│   └── backfill.py                ← seeds DB with historical simulation data
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Database Schema

```sql
-- raw forecast data from Open-Meteo
CREATE TABLE forecasts (
    id               SERIAL PRIMARY KEY,
    fetched_at       TIMESTAMPTZ NOT NULL,
    forecast_hour    TIMESTAMPTZ NOT NULL,
    max_wind_mph     FLOAT,
    wind_dir_deg     FLOAT,
    -- wind speed + direction at 19 altitudes (38 columns total)
    wind_speed_110   FLOAT,  wind_dir_110   FLOAT,
    wind_speed_320   FLOAT,  wind_dir_320   FLOAT,
    wind_speed_500   FLOAT,  wind_dir_500   FLOAT,
    wind_speed_800   FLOAT,  wind_dir_800   FLOAT,
    wind_speed_1000  FLOAT,  wind_dir_1000  FLOAT,
    wind_speed_1500  FLOAT,  wind_dir_1500  FLOAT,
    wind_speed_1900  FLOAT,  wind_dir_1900  FLOAT,
    wind_speed_3200  FLOAT,  wind_dir_3200  FLOAT,
    wind_speed_4200  FLOAT,  wind_dir_4200  FLOAT,
    wind_speed_5600  FLOAT,  wind_dir_5600  FLOAT,
    wind_speed_7200  FLOAT,  wind_dir_7200  FLOAT,
    wind_speed_9200  FLOAT,  wind_dir_9200  FLOAT,
    wind_speed_10400 FLOAT,  wind_dir_10400 FLOAT,
    wind_speed_11800 FLOAT,  wind_dir_11800 FLOAT,
    wind_speed_13500 FLOAT,  wind_dir_13500 FLOAT,
    wind_speed_15800 FLOAT,  wind_dir_15800 FLOAT,
    wind_speed_17700 FLOAT,  wind_dir_17700 FLOAT,
    wind_speed_19300 FLOAT,  wind_dir_19300 FLOAT,
    wind_speed_22000 FLOAT,  wind_dir_22000 FLOAT
);

-- one prediction per forecast hour
CREATE TABLE predictions (
    id                  SERIAL PRIMARY KEY,
    forecast_id         INTEGER REFERENCES forecasts(id),
    predicted_at        TIMESTAMPTZ NOT NULL,
    forecast_hour       TIMESTAMPTZ NOT NULL,
    -- dispersion math outputs
    landing_lat         FLOAT,
    landing_lon         FLOAT,
    predicted_dist_nm   FLOAT,
    ellipse_major_deg   FLOAT,
    ellipse_minor_deg   FLOAT,
    ellipse_tilt_deg    FLOAT,
    -- ML outputs
    p_safe_launch       FLOAT,       -- 0.0 to 1.0
    go_no_go            BOOLEAN,     -- threshold at 0.80
    top_risk_altitude   INTEGER,     -- altitude ft with highest feature importance
    top_risk_factor     FLOAT
);
```

---

## API Routes

```
GET  /api/predictions/latest
     Returns next 24 hours of predictions
     Powers the main dashboard on load

GET  /api/predictions/history?days=30
     Historical predictions for time series chart

GET  /api/predictions/{forecast_hour}
     Detail for one specific hour
     Powers ForecastCard on TimelineBar click

GET  /api/weather/current
     Raw current wind profile
     Powers WindProfileChart

GET  /api/health
     Last pipeline run time, prediction count, status
```

---

## The Hourly Pipeline

```python
# pipeline.py — simplified

async def run_pipeline():
    # 1. fetch next 24hrs from Open-Meteo
    forecasts = await fetch_forecast(lat=47.965378, lon=-81.873536)

    for forecast in forecasts:
        # 2. save raw forecast
        forecast_id = await save_forecast(forecast)

        # 3. dispersion math → landing zone
        landing_zone = run_dispersion(forecast.wind_profile)

        # 4. ML classifier → P(safe)
        p_safe = ml_model.predict_proba(build_features(forecast))[0][1]

        # 5. save prediction
        await save_prediction(
            forecast_id=forecast_id,
            landing_zone=landing_zone,
            p_safe=p_safe,
            go_no_go=p_safe >= 0.80
        )
```

---

## Open-Meteo Endpoint

```
https://api.open-meteo.com/v1/forecast
  ?latitude=47.965378
  &longitude=-81.873536
  &hourly=windspeed_10m,winddirection_10m,
           windspeed_80m,winddirection_80m,
           windspeed_120m,winddirection_120m,
           windspeed_180m,winddirection_180m
  &wind_speed_unit=mph
  &forecast_days=2
  &timezone=America/Toronto

Free. No API key. No rate limit for reasonable use.
Note: Open-Meteo altitude levels do not map exactly to the
19 simulation altitudes — feature engineering in features.py
handles interpolation or nearest-altitude mapping.
```

---

## ML Layer

### Problem framing
Binary classification: given a wind profile, predict whether a rocket lands within 10 NM.

### Features
38 features per forecast hour:
- Wind speed at each of 19 altitudes (mph)
- Wind direction at each of 19 altitudes (degrees)
- Plus max_wind_speed as a summary feature (39 total)

### Model
XGBoost classifier. Chosen because:
- Industry standard for tabular data
- Outperforms neural networks on small tabular datasets
- Built-in feature importance
- Fast inference

### Training data
Historical simulation CSVs. Each row = one simulated flight.
Label = `within_safe_zone` (bool, derived from haversine distance < 10 NM).

### Evaluation metric
AUC-ROC via 5-fold cross-validation. Not accuracy — class imbalance likely (most flights land safely).

### Serialization
```python
import joblib
joblib.dump(model, 'backend/ml/model.joblib')
model = joblib.load('backend/ml/model.joblib')
```

### Feature importance output
Top risk altitude = the altitude column with the highest contribution to the current prediction. Displayed in `FeatureImportance.jsx` and `ForecastCard.jsx`.

---

## Frontend Component Responsibilities

| Component | Data source | What it shows |
|---|---|---|
| `SafetyGauge` | `predictions[currentHour].p_safe_launch` | Big P(safe) number, GO/NO-GO label, color coded |
| `TimelineBar` | `predictions[]` (24 items) | 24 clickable hour slots, green/yellow/red |
| `MapPanel` | `predictions[selectedHour]` | Leaflet map, launch site, 10NM circle, landing ellipse |
| `ForecastCard` | `predictions[selectedHour]` | Distance, top risk altitude, wind dir |
| `WindProfileChart` | `forecasts[selectedHour]` | Altitude vs wind speed, Chart.js horizontal bar |
| `FeatureImportance` | `predictions[selectedHour]` | Top 5 risk altitudes, bar chart |
| `HistoryChart` | `/api/predictions/history` | 30-day p_safe time series, Recharts |

---

## usePredictions Hook

```javascript
// hooks/usePredictions.js
import { useState, useEffect } from 'react'

export function usePredictions() {
    const [predictions, setPredictions] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [lastUpdated, setLastUpdated] = useState(null)

    const fetchPredictions = async () => {
        try {
            const res = await fetch('/api/predictions/latest')
            if (!res.ok) throw new Error('Failed to fetch')
            const data = await res.json()
            setPredictions(data)
            setLastUpdated(new Date())
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchPredictions()
        const interval = setInterval(fetchPredictions, 15 * 60 * 1000)
        return () => clearInterval(interval)
    }, [])

    return { predictions, loading, error, lastUpdated, refresh: fetchPredictions }
}
```

---

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Launch Window Dashboard        Last updated: 14 mins ago 🟢│
├──────────────────────────────────┬──────────────────────────┤
│                                  │  P(Safe Launch)          │
│   MapPanel (react-leaflet)       │                          │
│   - Launch site marker           │       87%                │
│   - 10 NM red dashed circle      │   ████████░░  GO         │
│   - Landing ellipse (blue)       │                          │
│                                  │  Top risk: 3200ft winds  │
│                                  │  Landing dist: 4.2 NM    │
├──────────────────────────────────┴──────────────────────────┤
│  Next 24 Hours (TimelineBar)                                │
│  [GO ][GO ][GO ][MARG][NO ][NO ][GO ][GO ]...              │
│   6am  7am  8am  9am  10am 11am  12pm  1pm                 │
├──────────────────────────────────┬──────────────────────────┤
│  WindProfileChart (Chart.js)     │  HistoryChart (Recharts) │
│  Altitude vs wind speed          │  30-day p_safe trend     │
│  Horizontal bar + direction      │  Line chart              │
└──────────────────────────────────┴──────────────────────────┘
```

---

## 65-Day Timeline

| Days | Phase | Done means |
|---|---|---|
| 1-3 | JS fundamentals | Can write map/filter/fetch from scratch |
| 4-7 | React tutorial | Can explain useState, useEffect, props without notes |
| 8-10 | Mini weather app | Independent React app fetching Open-Meteo |
| 11-13 | Project setup + DB | PostgreSQL running, schema created, can insert/read rows |
| 14-17 | Weather API | fetch_forecast() returns clean parsed data |
| 18-20 | Pipeline + scheduler | Hourly job runs, data lands in DB, no duplicates |
| 21-24 | Dispersion integration | run_prediction() works with forecast dict input |
| 25-28 | API routes | All 4 routes return real data, tested in /docs |
| 29-30 | CORS + connection | Frontend can fetch from backend |
| 31 | Vite setup | Blank React app with Tailwind running |
| 32 | App layout | Two-column skeleton |
| 33 | usePredictions | Hook fetches and auto-refreshes |
| 34-35 | SafetyGauge + TimelineBar | Core UI visible |
| 36-38 | MapPanel | Leaflet map with ellipse |
| 39-41 | WindProfileChart | Chart.js altitude chart |
| 42-44 | HistoryChart + ForecastCard | All components built |
| 45 | Wired together | Full end-to-end working |
| 46-49 | ML notebook | Model trained, AUC measured, saved to joblib |
| 50-52 | ML in pipeline | p_safe stored in DB every hour |
| 53-55 | ML in frontend | FeatureImportance component, updated SafetyGauge |
| 56-58 | Robustness | Error handling, empty states, duplicate prevention |
| 59-61 | Backfill | DB seeded with historical data, HistoryChart has data |
| 62-63 | README | Clone-and-run instructions, architecture diagram |
| 64-65 | Demo recording | 3-min screen recording, posted to LinkedIn |

### Hard cut rules if behind schedule
- Behind on Day 30 → cut ML layer entirely
- Behind on Day 45 → cut HistoryChart
- Never cut: pipeline → DB → API → map (the core loop)

---

## How to Use AI Assistance

### The core rule
Always write code first, even if wrong. Use AI to resolve specific stuck points, not to generate code to copy.

### Effective prompts
```
Learning concepts:
"Explain [X] like I know Python but not JS. Use a Python analogy."
"Quiz me on [X] with three questions. Don't give answers yet."

Code review:
"Here's my [component]. Review for correctness, React best
 practices, and one thing to improve."

Debugging:
"Here's my code [paste]. I expect [X]. Instead I get [Y].
 Here's what I've tried. What am I misunderstanding?"

Architecture:
"I'm thinking of [approach]. Here's my reasoning. What's
 wrong with this and what would you do instead?"
```

### Never do
- Paste code you can't explain line by line
- Use AI to skip understanding fundamentals
- Ask AI to pick the stack or architecture

---

## What This Project Demonstrates

| Skill area | Evidence |
|---|---|
| Data engineering | ETT pipeline, scheduled jobs, time-series DB schema, external API integration |
| Software engineering | REST API design, React frontend, database modeling, end-to-end system |
| ML engineering | Feature engineering, model training + evaluation, model serving via API |
| Domain knowledge | Applied rocketry dispersion math, haversine, covariance ellipses |

---

## Interview Talking Points

- "I built a system that fetches weather forecasts hourly for our launch site, runs them through our existing dispersion model, and shows the team which hours are safe to launch"
- "The ML layer is trained on historical simulation data — XGBoost classifier with 38 wind profile features across 19 altitudes — outputting a probability rather than a binary threshold"
- "Feature importance analysis showed that winds at [X]ft altitude drive most outlier landings, which matches what our flight dynamics team suspected"
- "The frontend auto-refreshes every 15 minutes and the map shows the predicted landing ellipse updating in real time as new forecasts come in"

---

## docker-compose.yml

```yaml
services:
  db:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: launchwindow
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## requirements.txt

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
apscheduler
httpx
pandas
numpy
scipy
xgboost
scikit-learn
joblib
python-multipart
```

---

## package.json dependencies

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-leaflet": "^4.0.0",
    "leaflet": "^1.9.0",
    "chart.js": "^4.0.0",
    "react-chartjs-2": "^5.0.0",
    "recharts": "^2.0.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^3.0.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0"
  }
}
```

---

## Key Decisions Already Made

| Decision | Choice | Reason |
|---|---|---|
| Frontend framework | React + Vite | Job market relevance |
| Styling | Tailwind CSS | Utility-first, fast iteration |
| Map | react-leaflet | Real tiles, zoom/pan, free |
| Charts | Chart.js + Recharts | Chart.js for wind profile, Recharts for time series |
| Backend | FastAPI | Python-native, async, auto docs |
| Database | PostgreSQL (TimescaleDB) | Time-series optimized, standard SQL |
| ML model | XGBoost | Best for tabular data, interpretable |
| Scheduler | APScheduler | Lightweight, runs inside FastAPI process |
| Weather API | Open-Meteo | Free, no key, reliable |
| JS minimalism | No Redux, no React Query | Overkill for this project size |

---

## Current Status

_Update this section as you make progress._

```
[ ] Days 1-10   JS + React fundamentals
[ ] Days 11-20  Backend pipeline
[ ] Days 21-30  Dispersion integration + API
[ ] Days 31-45  React frontend
[ ] Days 46-55  ML layer
[ ] Days 56-65  Polish + documentation
```

Last completed: _not started_
Currently working on: _JS fundamentals_
Blockers: _none_
