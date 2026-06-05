# Instagram Influencer Impact Analysis

A Flask-based demo application for analyzing Instagram influencer performance using sample post data. The project combines engagement metrics, fake follower estimation, sentiment analysis, and brand collaboration suggestions in a simple web dashboard.

## Features

- Analyze influencer engagement, reach, growth indicators, and posting consistency
- Estimate fake followers and overall credibility scores
- Run comment and caption sentiment analysis
- View dashboard charts and per-influencer summaries
- Generate niche-based brand collaboration recommendations
- Use sample CSV data by default, with support for Instagram Graph API collection scaffolding

## Tech Stack

- Python
- Flask
- Pandas, NumPy, scikit-learn
- TextBlob and NLTK
- Plotly and Matplotlib
- HTML, CSS, JavaScript
- Chart.js

## Project Structure

```text
instagram_influencer/
|-- app.py
|-- config.py
|-- requirements.txt
|-- setup.py
|-- data/
|   |-- sample_data.csv
|   `-- users.json
|-- modules/
|   |-- auth.py
|   |-- brand_recommendation.py
|   |-- data_collection.py
|   |-- data_preprocessing.py
|   |-- fake_follower_detection.py
|   |-- metrics_computation.py
|   |-- sentiment_analysis.py
|   `-- user_search.py
|-- static/
|   |-- css/style.css
|   `-- js/
|       |-- auth.js
|       |-- dashboard.js
|       `-- search.js
`-- templates/
    |-- dashboard.html
    |-- login.html
    |-- profile.html
    `-- signup.html
```

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

If your environment does not already include them, you may also need:

```powershell
pip install scipy PyJWT
```

### 3. Optional setup helper

The project includes a setup script that creates folders, prepares a `.env`, and installs dependencies:

```powershell
python setup.py
```

### 4. Run the application

```powershell
python app.py
```

Open `http://localhost:5000` in your browser.

## Pages

- `/` - login page
- `/signup` - signup page
- `/dashboard` - analytics dashboard
- `/profile` - user profile page

## API Endpoints

- `POST /api/analyze` - analyze all influencers in the sample dataset
- `GET /api/influencers` - list available influencer names
- `GET /api/influencer/<name>` - fetch analysis for one influencer

## Sample Data

The app uses `data/sample_data.csv` by default. The current sample dataset includes these influencer names:

- `ViratKohli`
- `PriyankaChopra`
- `AliaBhatt`
- `ShraddhaKapoor`
- `DeepikaPadukone`
- `NehaKakkar`

From the dashboard, you can:

- Click `Analyze All Influencers` to generate full dashboard metrics
- Search for one of the sample usernames to view detailed profile analytics

## Configuration

Environment variables are loaded from `.env` through `config.py`. Useful settings include:

- `SECRET_KEY`
- `DEBUG`
- `DATABASE_TYPE`
- `SAMPLE_DATA_PATH`
- `INSTAGRAM_ACCESS_TOKEN`
- `INSTAGRAM_CLIENT_ID`
- `INSTAGRAM_CLIENT_SECRET`
- `ENGAGEMENT_RATE_THRESHOLD`
- `CREDIBILITY_THRESHOLD`
- `ANOMALY_CONTAMINATION`

## Notes

- The current dashboard experience is centered on sample/demo data.
- Brand recommendations are rule-based suggestions derived from influencer niche and metrics.
- The frontend login/signup flow is currently demo-oriented and stores session data in browser `localStorage`.
- `modules/data_collection.py` contains scaffolding for Instagram Graph API data collection if credentials are added later.
