# Project: Apple of Fortune - 2025 Wrapped

## Project Context

This is a Spotify-inspired year-wrapped web application showcasing 2025 statistics for the "Apple of Fortune" Android mobile game, with comparisons to 2024 data. Built for the Tessl x Anthropic After-Work Hack 2025.

**Key Characteristics:**
- Zero external dependencies (no npm, no frameworks)
- Pure vanilla Python, HTML, CSS, JavaScript
- Mobile-first responsive design
- Sarcastic/humorous tone throughout
- Processes 7 CSV data sources from Google Play Console

## Important Context for Agents

### When Processing Data
- **Cumulative Tracking**: User acquisition must be calculated cumulatively (running sum)
- **Multiple Encodings**: AdMob data is UTF-16 tab-delimited, others are UTF-8 CSV
- **Date Formats**: Two formats used - "DD Mon YYYY" and "YYYY-MM-DD"
- **Year Filtering**: Separate 2024 and 2025 data for comparisons

### When Modifying Frontend
- **Consistent Pattern**: Every section should follow: 2025 metric → 2024 comparison → totals
- **No Emojis in Code**: Unless user explicitly requests
- **Sarcastic Tone**: Keep humor self-deprecating about the app being free/offline
- **Text Contrast**: Use multiple shadow layers for readability
- **Animations**: Fade-in and pop-in effects with staggered delays

### When Adding Features
- **No Libraries**: Keep everything vanilla - no jQuery, React, Bootstrap, etc.
- **Mobile First**: Test responsiveness, use clamp() for font sizes
- **File Sync**: Keep both `/index.html` and `/frontend/index.html` in sync
- **Data Source**: Always load from `../data/insights.json`

### Style Guidelines
- Gradient backgrounds (12 different color schemes)
- Border radius: 25-30px for images, 15-25px for cards
- Box shadows: Multiple layers for depth
- Font sizes: Use clamp() for responsive scaling
- Animations: 0.3s-0.8s durations

## Current Statistics (October 2025)

- **Total Players**: 418,755 (cumulative)
- **2025 New Players**: 130,119
- **Average DAU**: 2,075
- **Average MAU**: 19,437
- **Google Play Rating**: 4.04
- **Daily Earnings**: $5.45
- **Top Country**: Egypt (139,440 players)

## Testing Checklist

When making changes, verify:
- [ ] Data loads correctly from insights.json
- [ ] All sections have 2024 vs 2025 comparisons
- [ ] Text is readable with proper shadows
- [ ] Hover effects work on cards
- [ ] Mobile responsive (test at 320px, 768px, 1024px)
- [ ] Animations trigger on scroll
- [ ] Progress bar updates as you scroll
- [ ] Images load with rounded corners

# Usage Specs <!-- tessl-managed -->

[Usage specs](.tessl/framework/usage-specs.md) provide important context for third-party dependencies: @.tessl/framework/usage-specs.md

# Agent Rules <!-- tessl-managed -->

@RULES.md follow the [instructions](RULES.md)

# Knowledge Index <!-- tessl-managed -->

Documentation for dependencies and processes can be found in the [Knowledge Index](./KNOWLEDGE.md)