#!/usr/bin/env python3
"""
Analyze Apple of Fortune game statistics and generate insights for Year Wrapped 2025
"""

import csv
import json
from datetime import datetime
from collections import defaultdict
import statistics

def parse_number(value):
    """Parse number string with commas as thousands separator"""
    if not value or value == '-':
        return 0
    return int(value.replace(',', ''))

def parse_date(date_str):
    """Parse date string to datetime object"""
    # Handle both "Sep" and "Sept" formats
    date_str = date_str.replace('Sept', 'Sep')
    return datetime.strptime(date_str, '%d %b %Y')

def analyze_data(csv_path):
    """Analyze the CSV data and extract insights"""

    data_2024 = []
    data_2025 = []

    # Read and parse CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])

                # Extract key metrics
                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'total_installed': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): All countries / regions', '0')),
                    'total_dau': parse_number(row.get('Daily active users (DAU) (Unique users, Per interval, Daily): All countries / regions', '0')),
                    'egypt': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): Egypt', '0')),
                    'cote_ivoire': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): Côte d\'Ivoire', '0')),
                    'senegal': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): Senegal', '0')),
                    'uk': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): United Kingdom', '0')),
                    'us': parse_number(row.get('Installed audience (All users, Unique users, Per interval, Daily): United States', '0')),
                }

                # Categorize by year
                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error parsing row: {e}")
                continue

    # Calculate insights
    insights = {
        '2024': calculate_year_stats(data_2024, 2024),
        '2025': calculate_year_stats(data_2025, 2025),
        'comparisons': {}
    }

    # Calculate year-over-year comparisons
    if data_2024 and data_2025:
        insights['comparisons'] = calculate_comparisons(insights['2024'], insights['2025'])

    return insights

def calculate_year_stats(data, year):
    """Calculate statistics for a given year"""
    if not data:
        return {}

    # Sort by date
    data.sort(key=lambda x: x['date'])

    # Basic stats
    start_users = data[0]['total_installed']
    end_users = data[-1]['total_installed']
    peak_users = max(d['total_installed'] for d in data)
    peak_date = max(data, key=lambda x: x['total_installed'])['date_str']

    # DAU stats (filter out zeros)
    dau_values = [d['total_dau'] for d in data if d['total_dau'] > 0]
    avg_dau = int(statistics.mean(dau_values)) if dau_values else 0
    peak_dau = max(dau_values) if dau_values else 0
    peak_dau_date = max([d for d in data if d['total_dau'] > 0],
                         key=lambda x: x['total_dau'])['date_str'] if dau_values else 'N/A'

    # Growth
    total_growth = end_users - start_users
    growth_rate = ((end_users - start_users) / start_users * 100) if start_users > 0 else 0

    # Monthly breakdown
    monthly_stats = defaultdict(lambda: {'installs': [], 'dau': []})
    for record in data:
        month_key = record['date'].strftime('%B')
        monthly_stats[month_key]['installs'].append(record['total_installed'])
        if record['total_dau'] > 0:
            monthly_stats[month_key]['dau'].append(record['total_dau'])

    # Find best month (highest average DAU)
    best_month = None
    best_month_avg_dau = 0
    for month, stats in monthly_stats.items():
        if stats['dau']:
            avg = statistics.mean(stats['dau'])
            if avg > best_month_avg_dau:
                best_month_avg_dau = avg
                best_month = month

    # Country breakdown (using final values)
    final_record = data[-1]
    country_stats = {
        'Egypt': final_record['egypt'],
        'Côte d\'Ivoire': final_record['cote_ivoire'],
        'Senegal': final_record['senegal'],
        'United Kingdom': final_record['uk'],
        'United States': final_record['us']
    }

    # Calculate engagement rate (DAU/Installed)
    engagement_rates = []
    for record in data:
        if record['total_installed'] > 0 and record['total_dau'] > 0:
            rate = (record['total_dau'] / record['total_installed']) * 100
            engagement_rates.append(rate)

    avg_engagement = statistics.mean(engagement_rates) if engagement_rates else 0

    return {
        'year': year,
        'data_points': len(data),
        'date_range': f"{data[0]['date_str']} to {data[-1]['date_str']}",
        'start_users': start_users,
        'end_users': end_users,
        'peak_users': peak_users,
        'peak_date': peak_date,
        'total_growth': total_growth,
        'growth_rate': round(growth_rate, 2),
        'avg_dau': avg_dau,
        'peak_dau': peak_dau,
        'peak_dau_date': peak_dau_date,
        'best_month': best_month,
        'best_month_avg_dau': int(best_month_avg_dau),
        'avg_engagement_rate': round(avg_engagement, 2),
        'country_stats': country_stats,
        'monthly_breakdown': {month: {
            'avg_installs': int(statistics.mean(stats['installs'])),
            'avg_dau': int(statistics.mean(stats['dau'])) if stats['dau'] else 0
        } for month, stats in monthly_stats.items()}
    }

def calculate_comparisons(stats_2024, stats_2025):
    """Calculate year-over-year comparisons"""
    comparisons = {}

    # User growth comparison
    growth_2024 = stats_2024['total_growth']
    growth_2025 = stats_2025['total_growth']

    comparisons['user_growth_change'] = {
        '2024': growth_2024,
        '2025': growth_2025,
        'difference': growth_2025 - growth_2024,
        'change_pct': round(((growth_2025 - growth_2024) / abs(growth_2024) * 100) if growth_2024 != 0 else 0, 2)
    }

    # DAU comparison
    comparisons['dau_change'] = {
        '2024': stats_2024['avg_dau'],
        '2025': stats_2025['avg_dau'],
        'difference': stats_2025['avg_dau'] - stats_2024['avg_dau'],
        'change_pct': round(((stats_2025['avg_dau'] - stats_2024['avg_dau']) / stats_2024['avg_dau'] * 100) if stats_2024['avg_dau'] > 0 else 0, 2)
    }

    # Engagement comparison
    comparisons['engagement_change'] = {
        '2024': stats_2024['avg_engagement_rate'],
        '2025': stats_2025['avg_engagement_rate'],
        'difference': round(stats_2025['avg_engagement_rate'] - stats_2024['avg_engagement_rate'], 2),
        'change_pct': round(((stats_2025['avg_engagement_rate'] - stats_2024['avg_engagement_rate']) / stats_2024['avg_engagement_rate'] * 100) if stats_2024['avg_engagement_rate'] > 0 else 0, 2)
    }

    return comparisons

def main():
    # Use relative path from backend folder
    csv_path = '../data/app_stats.csv'

    print("🎮 Analyzing Apple of Fortune statistics...")
    print("=" * 60)

    insights = analyze_data(csv_path)

    # Save to JSON for use in web app
    with open('../data/insights.json', 'w') as f:
        json.dump(insights, f, indent=2)

    print("\n📊 2024 YEAR IN REVIEW")
    print("-" * 60)
    if insights['2024']:
        stats_2024 = insights['2024']
        print(f"Date Range: {stats_2024['date_range']}")
        print(f"Starting Users: {stats_2024['start_users']:,}")
        print(f"Ending Users: {stats_2024['end_users']:,}")
        print(f"Peak Users: {stats_2024['peak_users']:,} on {stats_2024['peak_date']}")
        print(f"Total Growth: {stats_2024['total_growth']:,} users ({stats_2024['growth_rate']}%)")
        print(f"Average Daily Active Users: {stats_2024['avg_dau']:,}")
        print(f"Peak DAU: {stats_2024['peak_dau']:,} on {stats_2024['peak_dau_date']}")
        print(f"Average Engagement Rate: {stats_2024['avg_engagement_rate']}%")
        print(f"Best Month: {stats_2024['best_month']} (avg DAU: {stats_2024['best_month_avg_dau']:,})")

    print("\n📊 2025 YEAR IN REVIEW (through October)")
    print("-" * 60)
    if insights['2025']:
        stats_2025 = insights['2025']
        print(f"Date Range: {stats_2025['date_range']}")
        print(f"Starting Users: {stats_2025['start_users']:,}")
        print(f"Ending Users: {stats_2025['end_users']:,}")
        print(f"Peak Users: {stats_2025['peak_users']:,} on {stats_2025['peak_date']}")
        print(f"Total Growth: {stats_2025['total_growth']:,} users ({stats_2025['growth_rate']}%)")
        print(f"Average Daily Active Users: {stats_2025['avg_dau']:,}")
        print(f"Peak DAU: {stats_2025['peak_dau']:,} on {stats_2025['peak_dau_date']}")
        print(f"Average Engagement Rate: {stats_2025['avg_engagement_rate']}%")
        print(f"Best Month: {stats_2025['best_month']} (avg DAU: {stats_2025['best_month_avg_dau']:,})")

        print("\n🌍 Country Breakdown (as of {})".format(stats_2025['date_range'].split(' to ')[1]))
        for country, users in sorted(stats_2025['country_stats'].items(), key=lambda x: x[1], reverse=True):
            if users > 0:
                pct = (users / stats_2025['end_users'] * 100) if stats_2025['end_users'] > 0 else 0
                print(f"  {country}: {users:,} ({pct:.1f}%)")

    print("\n📈 YEAR-OVER-YEAR COMPARISON")
    print("-" * 60)
    if insights['comparisons']:
        comp = insights['comparisons']

        print("User Growth:")
        ug = comp['user_growth_change']
        trend = "📈" if ug['difference'] > 0 else "📉"
        print(f"  2024: {ug['2024']:,} users")
        print(f"  2025: {ug['2025']:,} users")
        print(f"  Change: {trend} {ug['difference']:,} users ({ug['change_pct']:+.2f}%)")

        print("\nDaily Active Users:")
        dau = comp['dau_change']
        trend = "📈" if dau['difference'] > 0 else "📉"
        print(f"  2024: {dau['2024']:,} avg DAU")
        print(f"  2025: {dau['2025']:,} avg DAU")
        print(f"  Change: {trend} {dau['difference']:,} ({dau['change_pct']:+.2f}%)")

        print("\nEngagement Rate:")
        eng = comp['engagement_change']
        trend = "📈" if eng['difference'] > 0 else "📉"
        print(f"  2024: {eng['2024']}%")
        print(f"  2025: {eng['2025']}%")
        print(f"  Change: {trend} {eng['difference']:+.2f}% ({eng['change_pct']:+.2f}%)")

    print("\n✅ Insights saved to ../data/insights.json")
    print("=" * 60)

if __name__ == '__main__':
    main()
