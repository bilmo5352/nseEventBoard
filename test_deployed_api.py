"""
Test Deployed Railway API
==========================

Test the live API at nseeventboard-production.up.railway.app
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://nseeventboard-production.up.railway.app"


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint: /")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ API Name: {data.get('name')}")
        print(f"✅ Version: {data.get('version')}")
        print(f"\nAvailable Endpoints:")
        for endpoint, desc in data.get('endpoints', {}).items():
            print(f"  {endpoint}: {desc}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health():
    """Test health endpoint"""
    print_section("Testing Health Check: /health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"✅ Ready: {data.get('ready')}")
        print(f"✅ Timestamp: {data.get('timestamp')}")
        print(f"\nMonitors Status:")
        for monitor, status in data.get('monitors', {}).items():
            status_icon = "✅" if status else "⏳"
            print(f"  {status_icon} {monitor}: {'Ready' if status else 'Waiting...'}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_event_calendar():
    """Test event calendar endpoint"""
    print_section("Testing Event Calendar: /event-calendar")
    try:
        response = requests.get(f"{BASE_URL}/event-calendar?page=1&per_page=5", timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Response: {response.text}")
            return False
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Error: {data.get('error')}")
            return False
        
        metadata = data.get('metadata', {})
        pagination = data.get('pagination', {})
        
        print(f"\n✅ Metadata:")
        print(f"  - Scrape Time: {metadata.get('scrape_timestamp')}")
        print(f"  - Total Records: {metadata.get('total_records')}")
        print(f"  - Pages Scraped: {metadata.get('total_pages_scraped')}")
        
        print(f"\n✅ Pagination:")
        print(f"  - Page: {pagination.get('page')}/{pagination.get('total_pages')}")
        print(f"  - Per Page: {pagination.get('per_page')}")
        print(f"  - Total: {pagination.get('total_records')}")
        
        print(f"\n✅ Sample Events (first 3):")
        for i, event in enumerate(data.get('data', [])[:3], 1):
            symbol = event.get('SYMBOL', 'N/A')
            if isinstance(symbol, dict):
                symbol = symbol.get('text', 'N/A')
            company = event.get('COMPANY', 'N/A')
            purpose = event.get('PURPOSE', 'N/A')
            date = event.get('DATE', 'N/A')
            print(f"  {i}. {symbol} - {company}")
            print(f"     {purpose} on {date}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_announcements():
    """Test announcements endpoint"""
    print_section("Testing Announcements: /announcements (Equity)")
    try:
        response = requests.get(f"{BASE_URL}/announcements?market=equity&page=1&per_page=5", timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Response: {response.text}")
            return False
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Error: {data.get('error')}")
            return False
        
        metadata = data.get('metadata', {})
        pagination = data.get('pagination', {})
        
        print(f"\n✅ Metadata:")
        print(f"  - Market Type: {metadata.get('market_type')}")
        print(f"  - Total Records: {metadata.get('total_records')}")
        print(f"  - Scrape Time: {metadata.get('scrape_timestamp')}")
        
        print(f"\n✅ Pagination:")
        print(f"  - Total: {pagination.get('total_records')} records")
        
        print(f"\n✅ Sample Announcements (first 3):")
        for i, ann in enumerate(data.get('data', [])[:3], 1):
            symbol = ann.get('SYMBOL', 'N/A')
            if isinstance(symbol, dict):
                symbol = symbol.get('text', 'N/A')
            company = ann.get('COMPANY NAME', 'N/A')
            subject = ann.get('SUBJECT', 'N/A')
            print(f"  {i}. {symbol} - {company}")
            print(f"     {subject}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_crd():
    """Test CRD endpoint"""
    print_section("Testing CRD Credit Rating: /crd")
    try:
        response = requests.get(f"{BASE_URL}/crd?page=1&per_page=5", timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Response: {response.text}")
            return False
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Error: {data.get('error')}")
            return False
        
        metadata = data.get('metadata', {})
        pagination = data.get('pagination', {})
        
        print(f"\n✅ Metadata:")
        print(f"  - Total Records: {metadata.get('total_records')}")
        print(f"  - Scrape Time: {metadata.get('scrape_timestamp')}")
        
        print(f"\n✅ Sample Records (first 3):")
        for i, record in enumerate(data.get('data', [])[:3], 1):
            company = record.get('COMPANY NAME', 'N/A')
            if isinstance(company, dict):
                company = company.get('text', 'N/A')
            agency = record.get('NAME OF CREDIT RATING AGENCY', 'N/A')
            rating = record.get('CREDIT RATING', 'N/A')
            print(f"  {i}. {company}")
            print(f"     Rating: {rating} by {agency}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_credit_rating():
    """Test credit rating endpoint"""
    print_section("Testing Credit Rating Reg.30: /credit-rating (Equity)")
    try:
        response = requests.get(f"{BASE_URL}/credit-rating?market=equity&page=1&per_page=5", timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Response: {response.text}")
            return False
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Error: {data.get('error')}")
            return False
        
        metadata = data.get('metadata', {})
        pagination = data.get('pagination', {})
        
        print(f"\n✅ Metadata:")
        print(f"  - Market Type: {metadata.get('market_type')}")
        print(f"  - Total Records: {metadata.get('total_records')}")
        
        print(f"\n✅ Sample Records (first 3):")
        for i, record in enumerate(data.get('data', [])[:3], 1):
            symbol = record.get('SYMBOL', 'N/A')
            if isinstance(symbol, dict):
                symbol = symbol.get('text', 'N/A')
            company = record.get('COMPANY NAME', 'N/A')
            rating = record.get('CREDIT RATING', 'N/A')
            action = record.get('CURRENT ACTION', 'N/A')
            print(f"  {i}. {symbol} - {company}")
            print(f"     Rating: {rating} ({action})")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("NSE DATA API - LIVE DEPLOYMENT TEST")
    print("=" * 80)
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Root': test_root(),
        'Health': test_health(),
        'Event Calendar': test_event_calendar(),
        'Announcements': test_announcements(),
        'CRD': test_crd(),
        'Credit Rating': test_credit_rating()
    }
    
    # Summary
    print_section("TEST SUMMARY")
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    
    print("\nDetailed Results:")
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test}")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working perfectly!")
    elif passed > 0:
        print(f"\n⚠️  Partial success. {failed} endpoint(s) may still be initializing.")
        print("   Monitors need a few minutes to scrape initial data.")
    else:
        print("\n❌ All tests failed. Check Railway logs for errors.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

