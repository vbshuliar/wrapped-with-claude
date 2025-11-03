# Knowledge Index

## Project Overview

**Apple of Fortune - 2025 Wrapped** is a Spotify-inspired year-wrapped web application for an Android mobile game. Built for the Tessl x Anthropic After-Work Hack 2025.

### Technology Stack

- **Backend**: Python 3.x (vanilla, no external dependencies)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Data Processing**: CSV parsing with multiple encodings (UTF-8, UTF-16)
- **Data Format**: JSON for processed insights

### Key Features

- Long-scroll Spotify-style design with 14 animated sections
- Processes 7 different CSV data sources from Google Play Console
- Year-over-year comparisons (2024 vs 2025)
- Cumulative user acquisition tracking
- AdMob monetization metrics
- Responsive design (mobile-first approach)
- Sarcastic/humorous commentary throughout
- 12+ vibrant gradient backgrounds
- Smooth animations and transitions

## Data Sources

The application processes CSV files from Google Play Developer Console:

1. **user_acquisition.csv** - Daily new user sign-ups by country (UTF-8)
2. **dau.csv** - Daily Active Users metrics (UTF-8)
3. **mau.csv** - Monthly Active Users trends (UTF-8)
4. **installed_audience.csv** - Total installed user base (UTF-8)
5. **average_rating.csv** - Google Play rating over time (UTF-8)
6. **crashes.csv** - Daily crash counts by Android version (UTF-8)
7. **admob_report.csv** - AdMob monetization data (UTF-16 encoding, tab-delimited)

All files contain data from December 2023 through October 2025.

## Processing Pipeline

### Backend Script: `process_all_data.py`

The Python script processes all CSV files and generates `insights.json`:

```bash
cd backend
python3 process_all_data.py
```

**Key Functions:**
- `parse_date(date_str)` - Handles "DD Mon YYYY" format
- `parse_admob_date(date_str)` - Handles "YYYY-MM-DD" format
- `process_user_acquisition()` - Calculates cumulative totals and country breakdowns
- `process_dau()` - Analyzes daily active users
- `process_mau()` - Analyzes monthly active users
- `process_installed_audience()` - Tracks installed base
- `process_rating()` - Aggregates Google Play ratings
- `process_crashes()` - Summarizes crash statistics
- `process_admob()` - Processes UTF-16 encoded AdMob data with eCPM calculations
- `calculate_comparisons()` - Generates year-over-year metrics

### Frontend: `index.html`

Single-file web application with embedded CSS and JavaScript:

```bash
# Serve locally
python3 -m http.server 8000
# Visit http://localhost:8000/
```

**Design Patterns:**
- Each section follows: 2025 metric → 2024 comparison → totals/context
- Gradient backgrounds rotate through 12 color schemes
- Text shadows and box shadows for contrast
- Fade-in and pop-in animations on scroll
- Progress bar tracks scroll position

## Project Structure

```
wrapped-with-claude/
├── backend/
│   ├── analyze_data.py          # Legacy processor
│   └── process_all_data.py      # Main CSV processor
├── data/
│   ├── user_acquisition.csv
│   ├── dau.csv
│   ├── mau.csv
│   ├── installed_audience.csv
│   ├── average_rating.csv
│   ├── crashes.csv
│   ├── admob_report.csv
│   └── insights.json            # Generated output
├── frontend/
│   └── index.html               # Web application
├── images/
│   ├── logo.png                 # Game logo
│   ├── gameplay.webp            # Screenshot 1
│   └── gameplay2.webp           # Screenshot 2
├── index.html                   # Root copy
├── README.md
├── tessl.json                   # Tessl configuration
├── CLAUDE.md                    # Claude Code instructions
├── AGENTS.md                    # Agent rules
├── RULES.md                     # Registry rules
└── KNOWLEDGE.md                 # This file
```

## Development Workflow

1. **Update Data**: Place new CSV files in `data/` folder
2. **Process Data**: Run `python3 backend/process_all_data.py`
3. **View Results**: Open `index.html` in browser via HTTP server
4. **Iterate**: Modify frontend/backend as needed

## Key Metrics Displayed

### User Acquisition (Section 2-3)
- Total new players in 2025
- Cumulative player base
- Peak acquisition day
- Year-over-year comparison

### Engagement (Section 4-6)
- Average Daily Active Users (DAU)
- Peak engagement day
- Average Monthly Active Users (MAU)
- Year-over-year trends

### Quality (Section 7)
- Average Google Play rating
- Highest/lowest ratings in 2025
- Year-over-year rating change

### Global Reach (Section 8)
- Top countries: Egypt, Senegal, USA, UK
- Player counts per country

### Monetization (Section 9-10)
- Total ad impressions served
- Daily coffee money ($5.45/day average)
- Total 2025 earnings
- Year-over-year revenue comparison

## Design Philosophy

- **Sarcastic Tone**: Self-deprecating humor throughout
- **Free Game Emphasis**: Mentions it's $0, offline, no servers
- **Transparent Monetization**: Shows ads and revenue honestly
- **Year-over-Year Context**: Always compares 2024 vs 2025
- **Consistent Pattern**: Each section structured the same way

## No External Dependencies

This project intentionally uses no external libraries or frameworks:
- No npm/node_modules
- No Python packages beyond stdlib
- No CSS frameworks
- No JavaScript frameworks
- Pure vanilla code throughout

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive (tested on iOS and Android)
- Smooth scroll behavior
- CSS Grid and Flexbox
- CSS animations and transitions

