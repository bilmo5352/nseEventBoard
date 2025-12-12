"""
Fetch All NSE Data from Deployed API
=====================================

This script fetches ALL data from all 4 endpoints:
- Event Calendar
- Announcements (Equity, SME, Debt, MF)
- CRD Credit Rating
- Credit Rating Reg.30 (Equity, SME)

Usage:
    python fetch_all_data.py
"""

import requests
import json
import time
from datetime import datetime
import os

BASE_URL = "https://nseeventboard-production.up.railway.app"
OUTPUT_DIR = "fetched_data"


def create_output_dir():
    """Create output directory"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✅ Output directory: {OUTPUT_DIR}/")


def fetch_all_pages(endpoint, params=None):
    """
    Fetch all pages from an endpoint
    
    Args:
        endpoint: API endpoint (e.g., '/event-calendar')
        params: Additional query parameters
    
    Returns:
        dict: Combined data with metadata
    """
    if params is None:
        params = {}
    
    all_data = []
    page = 1
    total_pages = 1
    metadata = {}
    
    print(f"\n📊 Fetching from: {endpoint}")
    
    while page <= total_pages:
        try:
            # Add page and per_page to params
            params['page'] = page
            params['per_page'] = 1000  # Max per page
            
            # Make request
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Error {response.status_code} on page {page}")
                print(response.text)
                break
            
            data = response.json()
            
            # Check if successful
            if not data.get('success'):
                print(f"❌ API returned error: {data.get('error')}")
                break
            
            # Get metadata and pagination info
            metadata = data.get('metadata', {})
            pagination = data.get('pagination', {})
            total_pages = pagination.get('total_pages', 1)
            
            # Add page data
            page_data = data.get('data', [])
            all_data.extend(page_data)
            
            print(f"  ✅ Page {page}/{total_pages} - {len(page_data)} records ({len(all_data)} total)")
            
            page += 1
            time.sleep(0.5)  # Be nice to the server
            
        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break
    
    return {
        'metadata': metadata,
        'total_records': len(all_data),
        'fetched_at': datetime.now().isoformat(),
        'source': endpoint,
        'params': params,
        'data': all_data
    }


def save_to_json(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved: {filepath} ({len(data['data'])} records)")


def fetch_event_calendar():
    """Fetch all event calendar data"""
    print("\n" + "=" * 80)
    print("📅 FETCHING EVENT CALENDAR")
    print("=" * 80)
    
    data = fetch_all_pages('/event-calendar')
    save_to_json(data, 'event_calendar_all.json')
    return data


def fetch_announcements():
    """Fetch all announcements data for all markets"""
    print("\n" + "=" * 80)
    print("📢 FETCHING ANNOUNCEMENTS")
    print("=" * 80)
    
    markets = ['equity', 'sme', 'debt', 'mf']
    results = {}
    
    for market in markets:
        print(f"\n📊 Market: {market.upper()}")
        data = fetch_all_pages('/announcements', {'market': market})
        
        if data['total_records'] > 0:
            save_to_json(data, f'announcements_{market}_all.json')
            results[market] = data
        else:
            print(f"⚠️  No data available for {market}")
    
    return results


def fetch_crd():
    """Fetch all CRD credit rating data"""
    print("\n" + "=" * 80)
    print("💳 FETCHING CRD CREDIT RATING")
    print("=" * 80)
    
    data = fetch_all_pages('/crd')
    save_to_json(data, 'crd_all.json')
    return data


def fetch_credit_rating():
    """Fetch all credit rating reg.30 data for all markets"""
    print("\n" + "=" * 80)
    print("⭐ FETCHING CREDIT RATING REG.30")
    print("=" * 80)
    
    markets = ['equity', 'sme']
    results = {}
    
    for market in markets:
        print(f"\n📊 Market: {market.upper()}")
        data = fetch_all_pages('/credit-rating', {'market': market})
        
        if data['total_records'] > 0:
            save_to_json(data, f'credit_rating_{market}_all.json')
            results[market] = data
        else:
            print(f"⚠️  No data available for {market}")
    
    return results


def check_health():
    """Check API health before fetching"""
    print("\n" + "=" * 80)
    print("🏥 CHECKING API HEALTH")
    print("=" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        health = response.json()
        
        print(f"Status: {health.get('status')}")
        print(f"Ready: {health.get('ready')}")
        print(f"\nMonitors:")
        for monitor, status in health.get('monitors', {}).items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {monitor}")
        
        # Check if any monitors are ready
        monitors_ready = sum(health.get('monitors', {}).values())
        if monitors_ready == 0:
            print("\n⚠️  WARNING: No monitors are ready yet!")
            print("   The API may have just started. Wait a few minutes.")
            user_input = input("\nContinue anyway? (y/n): ")
            if user_input.lower() != 'y':
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def create_summary(results):
    """Create a summary of all fetched data"""
    summary = {
        'fetch_timestamp': datetime.now().isoformat(),
        'api_url': BASE_URL,
        'total_files': 0,
        'total_records': 0,
        'datasets': {}
    }
    
    # Event Calendar
    if 'event_calendar' in results:
        summary['datasets']['event_calendar'] = {
            'records': results['event_calendar']['total_records'],
            'file': 'event_calendar_all.json'
        }
        summary['total_records'] += results['event_calendar']['total_records']
        summary['total_files'] += 1
    
    # Announcements
    if 'announcements' in results:
        for market, data in results['announcements'].items():
            summary['datasets'][f'announcements_{market}'] = {
                'records': data['total_records'],
                'file': f'announcements_{market}_all.json'
            }
            summary['total_records'] += data['total_records']
            summary['total_files'] += 1
    
    # CRD
    if 'crd' in results:
        summary['datasets']['crd'] = {
            'records': results['crd']['total_records'],
            'file': 'crd_all.json'
        }
        summary['total_records'] += results['crd']['total_records']
        summary['total_files'] += 1
    
    # Credit Rating
    if 'credit_rating' in results:
        for market, data in results['credit_rating'].items():
            summary['datasets'][f'credit_rating_{market}'] = {
                'records': data['total_records'],
                'file': f'credit_rating_{market}_all.json'
            }
            summary['total_records'] += data['total_records']
            summary['total_files'] += 1
    
    # Save summary
    summary_path = os.path.join(OUTPUT_DIR, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    return summary


def print_summary(summary):
    """Print summary of fetched data"""
    print("\n" + "=" * 80)
    print("📊 FETCH SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Total Files: {summary['total_files']}")
    print(f"✅ Total Records: {summary['total_records']:,}")
    print(f"📁 Output Directory: {OUTPUT_DIR}/")
    
    print("\n📋 Datasets:")
    for name, info in summary['datasets'].items():
        print(f"  • {name}: {info['records']:,} records → {info['file']}")
    
    print("\n" + "=" * 80)


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("NSE DATA FETCHER - GET ALL DATA")
    print("=" * 80)
    print(f"API: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directory
    create_output_dir()
    
    # Check API health
    if not check_health():
        print("\n❌ Health check failed. Exiting.")
        return
    
    # Fetch all data
    results = {}
    
    try:
        # 1. Event Calendar
        results['event_calendar'] = fetch_event_calendar()
        
        # 2. Announcements (all markets)
        results['announcements'] = fetch_announcements()
        
        # 3. CRD
        results['crd'] = fetch_crd()
        
        # 4. Credit Rating (all markets)
        results['credit_rating'] = fetch_credit_rating()
        
        # Create and save summary
        summary = create_summary(results)
        print_summary(summary)
        
        print("\n🎉 ALL DATA FETCHED SUCCESSFULLY!")
        print(f"\nCheck the '{OUTPUT_DIR}/' folder for all JSON files.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Fetch interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

