import requests

url = "https://nseeventboard-production.up.railway.app"

print("Testing API...")
print("=" * 80)

# Test health
try:
    r = requests.get(f"{url}/health", timeout=10)
    print(f"✅ Health Check: {r.status_code}")
    print(r.json())
except Exception as e:
    print(f"❌ Health Error: {e}")

print("\n" + "=" * 80)

# Test event calendar
try:
    r = requests.get(f"{url}/event-calendar?page=1&per_page=3", timeout=15)
    print(f"✅ Event Calendar: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Total records: {data['pagination']['total_records']}")
        print(f"First event: {data['data'][0] if data['data'] else 'No data yet'}")
    else:
        print(r.json())
except Exception as e:
    print(f"❌ Event Calendar Error: {e}")

