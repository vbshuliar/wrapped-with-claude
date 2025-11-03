#!/usr/bin/env python3
"""
Process all Apple of Fortune CSV data files and generate comprehensive insights for Year Wrapped 2025
"""

import csv
import json
from datetime import datetime
from collections import defaultdict
import statistics
from pathlib import Path

def parse_number(value):
    """Parse number string with commas as thousands separator"""
    if not value or value == '-':
        return 0
    return int(value.replace(',', ''))

def parse_float(value):
    """Parse float value"""
    if not value or value == '-':
        return 0.0
    return float(value)

def parse_date(date_str):
    """Parse date string to datetime object"""
    date_str = date_str.replace('Sept', 'Sep')
    return datetime.strptime(date_str, '%d %b %Y')

def parse_admob_date(date_str):
    """Parse AdMob date string (YYYY-MM-DD format)"""
    return datetime.strptime(date_str, '%Y-%m-%d')

def process_user_acquisition(csv_path):
    """Process user acquisition data - CUMULATIVE per day"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Track cumulative counts
        cumulative_all = 0
        cumulative_egypt = 0
        cumulative_senegal = 0
        cumulative_cote = 0
        cumulative_uk = 0
        cumulative_us = 0

        for row in reader:
            try:
                date = parse_date(row['Date'])

                # Daily acquisitions
                daily_all = parse_number(row["User acquisition (All users, All events, Per interval, Daily): All countries / regions"])
                daily_egypt = parse_number(row.get("User acquisition (All users, All events, Per interval, Daily): Egypt", '0'))
                daily_senegal = parse_number(row.get("User acquisition (All users, All events, Per interval, Daily): Senegal", '0'))
                daily_cote = parse_number(row.get("User acquisition (All users, All events, Per interval, Daily): Côte d'Ivoire", '0'))
                daily_uk = parse_number(row.get("User acquisition (All users, All events, Per interval, Daily): United Kingdom", '0'))
                daily_us = parse_number(row.get("User acquisition (All users, All events, Per interval, Daily): United States", '0'))

                # Add to cumulative
                cumulative_all += daily_all
                cumulative_egypt += daily_egypt
                cumulative_senegal += daily_senegal
                cumulative_cote += daily_cote
                cumulative_uk += daily_uk
                cumulative_us += daily_us

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'daily_acquisition': daily_all,
                    'cumulative_acquisition': cumulative_all,
                    'egypt': cumulative_egypt,
                    'senegal': cumulative_senegal,
                    'cote_ivoire': cumulative_cote,
                    'uk': cumulative_uk,
                    'us': cumulative_us
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing user acquisition row: {e}")
                continue

    return analyze_acquisition(data_2024, data_2025)

def analyze_acquisition(data_2024, data_2025):
    """Analyze user acquisition data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        daily_acq = [d['daily_acquisition'] for d in data_2024]
        stats_2024 = {
            'total_acquired': data_2024[-1]['cumulative_acquisition'] - (data_2024[0]['cumulative_acquisition'] - data_2024[0]['daily_acquisition']),
            'avg_daily': int(statistics.mean(daily_acq)),
            'peak_day': max(data_2024, key=lambda x: x['daily_acquisition'])['date_str'],
            'peak_day_count': max(daily_acq),
            'final_cumulative': data_2024[-1]['cumulative_acquisition']
        }

    if data_2025:
        daily_acq = [d['daily_acquisition'] for d in data_2025]
        stats_2025 = {
            'total_acquired': data_2025[-1]['cumulative_acquisition'] - (data_2025[0]['cumulative_acquisition'] - data_2025[0]['daily_acquisition']),
            'avg_daily': int(statistics.mean(daily_acq)),
            'peak_day': max(data_2025, key=lambda x: x['daily_acquisition'])['date_str'],
            'peak_day_count': max(daily_acq),
            'final_cumulative': data_2025[-1]['cumulative_acquisition'],
            'countries': {
                'Egypt': data_2025[-1]['egypt'],
                'Senegal': data_2025[-1]['senegal'],
                'Côte d\'Ivoire': data_2025[-1]['cote_ivoire'],
                'United Kingdom': data_2025[-1]['uk'],
                'United States': data_2025[-1]['us']
            }
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_dau(csv_path):
    """Process Daily Active Users data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])
                dau = parse_number(row["Daily active users (DAU) (Unique users, Per interval, Daily): All countries / regions"])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'dau': dau
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing DAU row: {e}")
                continue

    return analyze_dau(data_2024, data_2025)

def analyze_dau(data_2024, data_2025):
    """Analyze DAU data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        dau_values = [d['dau'] for d in data_2024 if d['dau'] > 0]
        stats_2024 = {
            'avg_dau': int(statistics.mean(dau_values)),
            'peak_dau': max(dau_values),
            'peak_date': max(data_2024, key=lambda x: x['dau'])['date_str'],
            'min_dau': min(dau_values)
        }

    if data_2025:
        dau_values = [d['dau'] for d in data_2025 if d['dau'] > 0]
        stats_2025 = {
            'avg_dau': int(statistics.mean(dau_values)),
            'peak_dau': max(dau_values),
            'peak_date': max(data_2025, key=lambda x: x['dau'])['date_str'],
            'min_dau': min(dau_values)
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_mau(csv_path):
    """Process Monthly Active Users data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])
                mau = parse_number(row["Monthly active users (MAU) (Unique users, Per interval, Daily): All countries / regions"])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'mau': mau
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing MAU row: {e}")
                continue

    return analyze_mau(data_2024, data_2025)

def analyze_mau(data_2024, data_2025):
    """Analyze MAU data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        mau_values = [d['mau'] for d in data_2024 if d['mau'] > 0]
        stats_2024 = {
            'avg_mau': int(statistics.mean(mau_values)),
            'peak_mau': max(mau_values),
            'peak_date': max(data_2024, key=lambda x: x['mau'])['date_str']
        }

    if data_2025:
        mau_values = [d['mau'] for d in data_2025 if d['mau'] > 0]
        stats_2025 = {
            'avg_mau': int(statistics.mean(mau_values)),
            'peak_mau': max(mau_values),
            'peak_date': max(data_2025, key=lambda x: x['mau'])['date_str']
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_installed_audience(csv_path):
    """Process installed audience data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])
                installed = parse_number(row["Installed audience (All users, Unique users, Per interval, Daily): All countries / regions"])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'installed': installed
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing installed audience row: {e}")
                continue

    return analyze_installed(data_2024, data_2025)

def analyze_installed(data_2024, data_2025):
    """Analyze installed audience"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        stats_2024 = {
            'start': data_2024[0]['installed'],
            'end': data_2024[-1]['installed'],
            'peak': max(d['installed'] for d in data_2024),
            'peak_date': max(data_2024, key=lambda x: x['installed'])['date_str']
        }

    if data_2025:
        stats_2025 = {
            'start': data_2025[0]['installed'],
            'end': data_2025[-1]['installed'],
            'peak': max(d['installed'] for d in data_2025),
            'peak_date': max(data_2025, key=lambda x: x['installed'])['date_str']
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_rating(csv_path):
    """Process average rating data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])
                rating = parse_float(row["Google Play rating (Per interval, Daily): All countries / regions"])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'rating': rating
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing rating row: {e}")
                continue

    return analyze_rating(data_2024, data_2025)

def analyze_rating(data_2024, data_2025):
    """Analyze rating data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        ratings = [d['rating'] for d in data_2024 if d['rating'] > 0]
        stats_2024 = {
            'avg_rating': round(statistics.mean(ratings), 2),
            'highest': round(max(ratings), 2),
            'lowest': round(min(ratings), 2)
        }

    if data_2025:
        ratings = [d['rating'] for d in data_2025 if d['rating'] > 0]
        stats_2025 = {
            'avg_rating': round(statistics.mean(ratings), 2),
            'highest': round(max(ratings), 2),
            'lowest': round(min(ratings), 2)
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_crashes(csv_path):
    """Process crash data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                date = parse_date(row['Date'])
                crashes = parse_number(row["Crashes (Per interval, Daily): All Android versions"])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'crashes': crashes
                }

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing crashes row: {e}")
                continue

    return analyze_crashes(data_2024, data_2025)

def analyze_crashes(data_2024, data_2025):
    """Analyze crash data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        crash_values = [d['crashes'] for d in data_2024]
        stats_2024 = {
            'total_crashes': sum(crash_values),
            'avg_daily': int(statistics.mean(crash_values)),
            'worst_day': max(data_2024, key=lambda x: x['crashes'])['date_str'],
            'worst_day_count': max(crash_values)
        }

    if data_2025:
        crash_values = [d['crashes'] for d in data_2025]
        stats_2025 = {
            'total_crashes': sum(crash_values),
            'avg_daily': int(statistics.mean(crash_values)),
            'worst_day': max(data_2025, key=lambda x: x['crashes'])['date_str'],
            'worst_day_count': max(crash_values)
        }

    return {'2024': stats_2024, '2025': stats_2025}

def process_admob(csv_path):
    """Process AdMob monetization data"""
    data_2024 = []
    data_2025 = []

    with open(csv_path, 'r', encoding='utf-16') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            try:
                date = parse_admob_date(row['Date'])

                record = {
                    'date': date,
                    'date_str': row['Date'],
                    'earnings': parse_float(row['Estimated earnings (USD)']),
                    'ecpm': parse_float(row['Observed eCPM (USD)']),
                    'requests': parse_number(row['Requests']),
                    'impressions': parse_number(row['Impressions']),
                    'clicks': parse_number(row['Clicks']),
                    'ctr': row.get('CTR', '0%').replace('%', '')
                }

                # Convert CTR to float
                try:
                    record['ctr'] = parse_float(record['ctr'])
                except:
                    record['ctr'] = 0.0

                if date.year == 2024:
                    data_2024.append(record)
                elif date.year == 2025:
                    data_2025.append(record)

            except Exception as e:
                print(f"Error processing AdMob row: {e}")
                continue

    return analyze_admob(data_2024, data_2025)

def analyze_admob(data_2024, data_2025):
    """Analyze AdMob data"""
    stats_2024 = {}
    stats_2025 = {}

    if data_2024:
        total_earnings = sum(d['earnings'] for d in data_2024)
        total_impressions = sum(d['impressions'] for d in data_2024)
        total_clicks = sum(d['clicks'] for d in data_2024)
        avg_ecpm = statistics.mean([d['ecpm'] for d in data_2024 if d['ecpm'] > 0])

        stats_2024 = {
            'total_earnings': round(total_earnings, 2),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'avg_ecpm': round(avg_ecpm, 2),
            'best_day': max(data_2024, key=lambda x: x['earnings'])['date_str'],
            'best_day_earnings': round(max(d['earnings'] for d in data_2024), 2),
            'avg_daily_earnings': round(statistics.mean([d['earnings'] for d in data_2024]), 2),
            'avg_daily_impressions': int(statistics.mean([d['impressions'] for d in data_2024]))
        }

    if data_2025:
        total_earnings = sum(d['earnings'] for d in data_2025)
        total_impressions = sum(d['impressions'] for d in data_2025)
        total_clicks = sum(d['clicks'] for d in data_2025)
        avg_ecpm = statistics.mean([d['ecpm'] for d in data_2025 if d['ecpm'] > 0])

        stats_2025 = {
            'total_earnings': round(total_earnings, 2),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'avg_ecpm': round(avg_ecpm, 2),
            'best_day': max(data_2025, key=lambda x: x['earnings'])['date_str'],
            'best_day_earnings': round(max(d['earnings'] for d in data_2025), 2),
            'avg_daily_earnings': round(statistics.mean([d['earnings'] for d in data_2025]), 2),
            'avg_daily_impressions': int(statistics.mean([d['impressions'] for d in data_2025]))
        }

    return {'2024': stats_2024, '2025': stats_2025}

def calculate_comparisons(insights):
    """Calculate year-over-year comparisons"""
    comparisons = {}

    # User acquisition comparison
    if insights['user_acquisition']['2024'] and insights['user_acquisition']['2025']:
        ua_2024 = insights['user_acquisition']['2024']['total_acquired']
        ua_2025 = insights['user_acquisition']['2025']['total_acquired']
        comparisons['user_acquisition'] = {
            '2024': ua_2024,
            '2025': ua_2025,
            'change_pct': round(((ua_2025 - ua_2024) / ua_2024 * 100) if ua_2024 > 0 else 0, 2)
        }

    # DAU comparison
    if insights['dau']['2024'] and insights['dau']['2025']:
        dau_2024 = insights['dau']['2024']['avg_dau']
        dau_2025 = insights['dau']['2025']['avg_dau']
        comparisons['dau'] = {
            '2024': dau_2024,
            '2025': dau_2025,
            'change_pct': round(((dau_2025 - dau_2024) / dau_2024 * 100) if dau_2024 > 0 else 0, 2)
        }

    # MAU comparison
    if insights['mau']['2024'] and insights['mau']['2025']:
        mau_2024 = insights['mau']['2024']['avg_mau']
        mau_2025 = insights['mau']['2025']['avg_mau']
        comparisons['mau'] = {
            '2024': mau_2024,
            '2025': mau_2025,
            'change_pct': round(((mau_2025 - mau_2024) / mau_2024 * 100) if mau_2024 > 0 else 0, 2)
        }

    # Rating comparison
    if insights['rating']['2024'] and insights['rating']['2025']:
        rating_2024 = insights['rating']['2024']['avg_rating']
        rating_2025 = insights['rating']['2025']['avg_rating']
        comparisons['rating'] = {
            '2024': rating_2024,
            '2025': rating_2025,
            'change': round(rating_2025 - rating_2024, 2)
        }

    # Crash comparison
    if insights['crashes']['2024'] and insights['crashes']['2025']:
        crash_2024 = insights['crashes']['2024']['avg_daily']
        crash_2025 = insights['crashes']['2025']['avg_daily']
        comparisons['crashes'] = {
            '2024': crash_2024,
            '2025': crash_2025,
            'change_pct': round(((crash_2025 - crash_2024) / crash_2024 * 100) if crash_2024 > 0 else 0, 2)
        }

    # AdMob comparisons
    if insights['admob']['2024'] and insights['admob']['2025']:
        earnings_2024 = insights['admob']['2024']['total_earnings']
        earnings_2025 = insights['admob']['2025']['total_earnings']
        impressions_2024 = insights['admob']['2024']['total_impressions']
        impressions_2025 = insights['admob']['2025']['total_impressions']

        comparisons['admob_earnings'] = {
            '2024': earnings_2024,
            '2025': earnings_2025,
            'change_pct': round(((earnings_2025 - earnings_2024) / earnings_2024 * 100) if earnings_2024 > 0 else 0, 2)
        }

        comparisons['admob_impressions'] = {
            '2024': impressions_2024,
            '2025': impressions_2025,
            'change_pct': round(((impressions_2025 - impressions_2024) / impressions_2024 * 100) if impressions_2024 > 0 else 0, 2)
        }

    return comparisons

def main():
    data_dir = Path('../data')

    print("🎮 Processing Apple of Fortune Year Wrapped 2025 Data...")
    print("=" * 70)

    insights = {}

    # Process each data source
    print("\n📊 Processing User Acquisition (Cumulative)...")
    insights['user_acquisition'] = process_user_acquisition(data_dir / 'user_acquisition.csv')

    print("👥 Processing Daily Active Users...")
    insights['dau'] = process_dau(data_dir / 'dau.csv')

    print("📅 Processing Monthly Active Users...")
    insights['mau'] = process_mau(data_dir / 'mau.csv')

    print("📱 Processing Installed Audience...")
    insights['installed_audience'] = process_installed_audience(data_dir / 'installed_audience.csv')

    print("⭐ Processing Ratings...")
    insights['rating'] = process_rating(data_dir / 'average_rating.csv')

    print("💥 Processing Crashes...")
    insights['crashes'] = process_crashes(data_dir / 'crashes.csv')

    print("💰 Processing AdMob Data...")
    insights['admob'] = process_admob(data_dir / 'admob_report.csv')

    # Calculate comparisons
    print("\n📈 Calculating Year-over-Year Comparisons...")
    insights['comparisons'] = calculate_comparisons(insights)

    # Save to JSON
    output_path = data_dir / 'insights.json'
    with open(output_path, 'w') as f:
        json.dump(insights, f, indent=2)

    print(f"\n✅ Insights saved to {output_path}")

    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)

    if insights['user_acquisition']['2025']:
        ua = insights['user_acquisition']['2025']
        print(f"\n🚀 User Acquisition (2025):")
        print(f"   Total Acquired: {ua['total_acquired']:,}")
        print(f"   Average Daily: {ua['avg_daily']:,}")
        print(f"   Peak Day: {ua['peak_day']} ({ua['peak_day_count']:,} users)")
        print(f"   Final Cumulative: {ua['final_cumulative']:,}")

    if insights['dau']['2025']:
        dau = insights['dau']['2025']
        print(f"\n👥 Daily Active Users (2025):")
        print(f"   Average: {dau['avg_dau']:,}")
        print(f"   Peak: {dau['peak_dau']:,} on {dau['peak_date']}")

    if insights['rating']['2025']:
        rating = insights['rating']['2025']
        print(f"\n⭐ Rating (2025):")
        print(f"   Average: {rating['avg_rating']}")
        print(f"   Highest: {rating['highest']}")

    if insights['crashes']['2025']:
        crashes = insights['crashes']['2025']
        print(f"\n💥 Crashes (2025):")
        print(f"   Total: {crashes['total_crashes']:,}")
        print(f"   Average Daily: {crashes['avg_daily']:,}")

    if insights['admob']['2025']:
        admob = insights['admob']['2025']
        print(f"\n💰 AdMob Monetization (2025):")
        print(f"   Total Earnings: ${admob['total_earnings']:,.2f}")
        print(f"   Total Impressions: {admob['total_impressions']:,}")
        print(f"   Average eCPM: ${admob['avg_ecpm']:.2f}")
        print(f"   Average Daily Earnings: ${admob['avg_daily_earnings']:.2f}")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
