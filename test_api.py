"""
Test API Client
===============

Simple script to test the NSE Data API.

Usage:
    python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 80)
    print("Testing Health Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_event_calendar():
    """Test event calendar endpoint"""
    print("\n" + "=" * 80)
    print("Testing Event Calendar Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/event-calendar?page=1&per_page=5")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nTotal Records: {data['pagination']['total_records']}")
    print(f"Page: {data['pagination']['page']}")
    print(f"Per Page: {data['pagination']['per_page']}")
    print(f"\nFirst 3 events:")
    for i, event in enumerate(data['data'][:3], 1):
        symbol = event.get('SYMBOL', 'N/A')
        if isinstance(symbol, dict):
            symbol = symbol.get('text', 'N/A')
        company = event.get('COMPANY', 'N/A')
        purpose = event.get('PURPOSE', 'N/A')
        print(f"  {i}. {symbol} - {company}: {purpose}")


def test_announcements():
    """Test announcements endpoint"""
    print("\n" + "=" * 80)
    print("Testing Announcements Endpoint (Equity)")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/announcements?market=equity&page=1&per_page=5")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nTotal Records: {data['pagination']['total_records']}")
    print(f"Page: {data['pagination']['page']}")
    print(f"Market Type: {data['metadata']['market_type']}")
    print(f"\nFirst 3 announcements:")
    for i, ann in enumerate(data['data'][:3], 1):
        symbol = ann.get('SYMBOL', 'N/A')
        if isinstance(symbol, dict):
            symbol = symbol.get('text', 'N/A')
        company = ann.get('COMPANY NAME', 'N/A')
        subject = ann.get('SUBJECT', 'N/A')
        print(f"  {i}. {symbol} - {company}: {subject}")


def test_crd():
    """Test CRD endpoint"""
    print("\n" + "=" * 80)
    print("Testing CRD Credit Rating Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/crd?page=1&per_page=5")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nTotal Records: {data['pagination']['total_records']}")
    print(f"Page: {data['pagination']['page']}")
    print(f"\nFirst 3 records:")
    for i, record in enumerate(data['data'][:3], 1):
        company = record.get('COMPANY NAME', 'N/A')
        if isinstance(company, dict):
            company = company.get('text', 'N/A')
        agency = record.get('NAME OF CREDIT RATING AGENCY', 'N/A')
        rating = record.get('CREDIT RATING', 'N/A')
        print(f"  {i}. {company}: {rating} by {agency}")


def test_credit_rating():
    """Test credit rating endpoint"""
    print("\n" + "=" * 80)
    print("Testing Credit Rating Reg.30 Endpoint (Equity)")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/credit-rating?market=equity&page=1&per_page=5")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nTotal Records: {data['pagination']['total_records']}")
    print(f"Page: {data['pagination']['page']}")
    print(f"Market Type: {data['metadata']['market_type']}")
    print(f"\nFirst 3 records:")
    for i, record in enumerate(data['data'][:3], 1):
        symbol = record.get('SYMBOL', 'N/A')
        if isinstance(symbol, dict):
            symbol = symbol.get('text', 'N/A')
        company = record.get('COMPANY NAME', 'N/A')
        rating = record.get('CREDIT RATING', 'N/A')
        action = record.get('CURRENT ACTION', 'N/A')
        print(f"  {i}. {symbol} - {company}: {rating} ({action})")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("NSE DATA API - TEST CLIENT")
    print("=" * 80)
    print("\nMake sure the API is running: python api.py")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Test all endpoints
        test_health()
        test_event_calendar()
        test_announcements()
        test_crd()
        test_credit_rating()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: python api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

