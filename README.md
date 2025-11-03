# Apple of Fortune - 2025 Wrapped

A Spotify-inspired year-wrapped web application for the Apple of Fortune Android game, showcasing 2025 statistics with comparisons to 2024.

**Hackathon Project**: Built for Tessl x Anthropic's After-Work Hack - experimenting with spec-driven AI development to generate year-in-review dashboards using Claude Code.

## Features

- **Beautiful Long-Scroll Design**: Spotify-style animated sections with smooth scrolling
- **Visual Assets**: Game logo and gameplay screenshots with rounded corners
- **Comprehensive Metrics**:
  - User Acquisition (cumulative tracking)
  - Daily Active Users (DAU)
  - Monthly Active Users (MAU)
  - Installed Audience
  - Google Play Ratings
  - App Stability (Crashes)
  - Global Reach (Top 4 countries)
  - **AdMob Monetization** (Impressions, Revenue, eCPM)
- **Year-over-Year Comparisons**: 2024 vs 2025 with percentage changes
- **Smooth Animations**: Fade-ins, pop-ins, and scroll progress
- **Responsive Design**: Works on desktop, tablet, and mobile
- **12+ Gradient Backgrounds**: Vibrant color schemes
- **Interactive Elements**: Hover effects, scroll indicators, progress bar
- **Enhanced Text Contrast**: Multiple shadow layers for readability
- **Consistent Section Pattern**: Every section follows 2025 metric → 2024 comparison → totals

## Project Structure

```
wrapped-with-claude/
├── backend/
│   ├── analyze_data.py          # Legacy single-file processor
│   └── process_all_data.py      # New comprehensive processor for all CSV files
├── data/
│   ├── user_acquisition.csv     # Daily new user acquisitions
│   ├── dau.csv                  # Daily Active Users
│   ├── mau.csv                  # Monthly Active Users
│   ├── installed_audience.csv   # Installed user base
│   ├── average_rating.csv       # Google Play ratings
│   ├── crashes.csv              # Daily crash counts
│   ├── admob_report.csv         # AdMob monetization data
│   └── insights.json            # Generated insights (created by backend script)
├── frontend/
│   └── index.html               # Web application
├── images/
│   ├── logo.png                 # Game logo
│   ├── gameplay.webp            # Gameplay screenshot 1
│   └── gameplay2.webp           # Gameplay screenshot 2
├── index.html                   # Copy in root for easier access
├── tessl.json                   # Tessl configuration
├── CLAUDE.md                    # Claude Code instructions
├── AGENTS.md                    # Agent rules and context
├── KNOWLEDGE.md                 # Knowledge index with full documentation
├── RULES.md                     # Registry rules
└── README.md                    # This file
```

## Quick Start

### 1. Generate Insights

Run the Python script to process all CSV files and generate insights:

```bash
cd backend
python3 process_all_data.py
```

This will:
- Process all 6 CSV data sources
- Calculate cumulative user acquisition
- Analyze 2024 and 2025 statistics
- Generate comprehensive `data/insights.json`
- Display a summary in the terminal

### 2. View the Wrapped

Open the web application in a browser:

```bash
# Option 1: From root directory
python3 -m http.server 8000
# Then visit http://localhost:8000/

# Option 2: Direct file open (may have CORS issues)
open index.html
```

### 3. Navigate

Simply scroll through the beautiful year-wrapped experience!
- **Smooth scroll** through all sections
- **Progress bar** at the top shows your position
- **Animated sections** appear as you scroll

## Key Insights from 2025

### User Acquisition
- **130,119** new players acquired in 2025
- **418,755** total cumulative players
- **Peak day**: May 3, 2025 with 1,491 new players
- **Average**: 474 new players per day

### Engagement
- **2,075** average daily active users
- **Peak DAU**: 3,099 on February 16, 2025
- **Average MAU**: Check your wrapped!

### Quality
- **4.04** average Google Play rating
- **Highest rating**: 4.34
- **Total crashes**: 19,747 in 2025
- **Average**: 72 crashes per day

### Monetization (AdMob)
- **$2,985.63** total earnings in 2025
- **813,589** total ad impressions
- **$4.18** average eCPM
- **$5.45** average daily earnings

### Global Reach (Top 4 Countries)
1. Egypt
2. Senegal
3. United States
4. United Kingdom

### Year-over-Year Trends
- User Acquisition: See comparisons in the wrapped
- Daily Active Users: See comparisons in the wrapped
- Monthly Active Users: See comparisons in the wrapped
- Rating: See comparisons in the wrapped
- Crashes: See comparisons in the wrapped

## Data Sources

The application processes 7 separate CSV files:

1. **user_acquisition.csv**: Daily new user sign-ups by country
2. **dau.csv**: Daily Active Users metrics
3. **mau.csv**: Monthly Active Users trends
4. **installed_audience.csv**: Total installed user base
5. **average_rating.csv**: Google Play rating over time
6. **crashes.csv**: Daily crash counts by Android version
7. **admob_report.csv**: AdMob monetization data (earnings, impressions, eCPM)

All files contain data from December 2023 through October 2025.

## Technical Details

### Backend (Python)
- Processes 7 CSV files independently
- Handles multiple date formats and encodings (UTF-16 for AdMob)
- Calculates cumulative metrics (user acquisition)
- Computes monetization metrics (eCPM, revenue)
- Computes year-over-year comparisons
- Generates comprehensive JSON insights
- Error handling for malformed data
- Zero external dependencies (pure Python stdlib)

### Frontend (HTML/CSS/JavaScript)
- **Pure vanilla JavaScript** - no dependencies
- **Responsive design** - mobile-first approach
- **CSS animations** - fade-ins, pop-ins, bounces
- **12+ gradient backgrounds** - vibrant Spotify-style colors
- **Long-scroll layout** - smooth scrolling experience
- **Progress indicator** - fixed top bar
- **Hover effects** - interactive card animations
- **Enhanced typography** - multiple text shadow layers
- **Optimized images** - rounded corners, smooth hover effects
- **Consistent patterns** - standardized section structure

### Design System
- **Logo**: 200px max-width, 30px border-radius
- **Screenshots**: 300px max-width, 25px border-radius
- **Cards**: 15-25px border-radius, multiple shadow layers
- **Fonts**: Clamp() for responsive scaling
- **Colors**: 12+ gradient backgrounds
- **Animations**: 0.3s-0.8s durations with staggered delays

## Customization

### Adding More Metrics

Edit `backend/process_all_data.py` to add new data processing:

```python
def process_new_metric(csv_path):
    # Your processing logic
    return {'2024': stats_2024, '2025': stats_2025}
```

### Changing Colors

Modify the gradient backgrounds in `index.html`:

```css
.gradient-1 { background: linear-gradient(135deg, #yourcolor1 0%, #yourcolor2 100%); }
```

### Adding Sections

Add new sections to the `renderWrapped()` function:

```javascript
<section class="gradient-X">
    <div class="emoji">🎯</div>
    <h2>Your Metric</h2>
    <div class="big-number">${yourValue}</div>
    <p class="subtitle">Description</p>
</section>
```

## Requirements

- **Python 3.x** (for data processing)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- No external dependencies required

## Development

Built with:
- Python 3 (data analysis)
- HTML5, CSS3, Vanilla JavaScript
- No frameworks or libraries
- Inspired by Spotify Wrapped

---

**Created for**: Tessl x Anthropic After-Work Hack 2025
**Powered by**: Claude Code (AI-assisted development)
