# NSE Data Scraper API

Real-time NSE India corporate data scraping API with 4 monitors that update every 5 minutes.

## 🎯 Features

- **4 Data Sources:**
  - Event Calendar (upcoming corporate events)
  - Announcements (corporate filings)
  - CRD Credit Rating (debt ratings)
  - Credit Rating Reg.30 (credit ratings)

- **Auto-updating:** Scrapes every 5 minutes
- **REST API:** Easy access via HTTP
- **Pagination:** Handle large datasets
- **Docker Ready:** Deploy anywhere
- **Railway Compatible:** One-click deploy

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run all monitors + API
python start_all.py
```

API available at: http://localhost:5000

### Docker

```bash
# Build and run
docker-compose up --build

# Access API
curl http://localhost:5000/health
```

### Deploy to Railway

```bash
railway login
railway init
railway up
```

See [DEPLOY.md](DEPLOY.md) for detailed instructions.

## 📊 API Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /` | API documentation | `/` |
| `GET /health` | Health check | `/health` |
| `GET /event-calendar` | Event calendar data | `/event-calendar?page=1` |
| `GET /announcements` | Announcements data | `/announcements?market=equity` |
| `GET /crd` | CRD credit rating | `/crd?page=1` |
| `GET /credit-rating` | Credit rating reg.30 | `/credit-rating?market=equity` |

### Query Parameters

- `page` - Page number (default: 1)
- `per_page` - Records per page (default: 50, max: 1000)
- `market` - Market type: equity, sme, debt, mf (default: equity)

### Example Response

```json
{
  "success": true,
  "metadata": {
    "scrape_timestamp": "2025-12-12T15:30:45",
    "total_records": 500,
    "market_type": "Equity"
  },
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total_records": 500,
    "total_pages": 10,
    "has_next": true,
    "has_prev": false
  },
  "data": [ ... ]
}
```

## 📁 Project Structure

```
EventScrapeAPI/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── railway.toml           # Railway config
├── start_all.py           # Start all services
├── api.py                 # Flask API
├── requirements.txt       # Dependencies
│
├── MONITORS (scrape every 5 min)
│   ├── event_calendar_monitor.py
│   ├── announcements_monitor.py
│   ├── crd_monitor.py
│   └── credit_rating_monitor.py
│
└── VIEWERS (optional, local use)
    ├── view_latest_data.py
    ├── view_announcements_data.py
    ├── view_crd_data.py
    └── view_credit_rating_data.py
```

## 🔧 Configuration

All monitors are pre-configured to:
- Run in headless mode
- Scrape every 5 minutes
- Default to Equity market
- Save data to JSON files

## 📖 Usage Examples

### Python
```python
import requests

response = requests.get('http://localhost:5000/event-calendar')
data = response.json()

for event in data['data']:
    print(f"{event['COMPANY']}: {event['PURPOSE']}")
```

### JavaScript
```javascript
fetch('http://localhost:5000/announcements?market=equity')
  .then(res => res.json())
  .then(data => console.log(data));
```

### cURL
```bash
curl http://localhost:5000/crd?page=1&per_page=100
```

## 🐳 Docker Commands

```bash
# Build
docker build -t nse-scraper .

# Run
docker run -p 5000:5000 nse-scraper

# With docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 🚂 Railway Deployment

1. Connect your GitHub repo to Railway
2. Railway will auto-detect Dockerfile
3. Deploy automatically
4. Get your public URL

Or use CLI:
```bash
railway login
railway init
railway up
```

## ⚙️ Environment Variables

No environment variables required. All settings are pre-configured.

Optional:
- `PORT` - API port (default: 5000)

## 📊 Data Sources

All data scraped from NSE India:
- https://www.nseindia.com/companies-listing/corporate-filings-event-calendar
- https://www.nseindia.com/companies-listing/corporate-filings-announcements
- https://www.nseindia.com/companies-listing/debt-centralised-database/crd
- https://www.nseindia.com/companies-listing/corporate-sdd-credit-rating-reg30

## 🔒 Legal

For educational purposes only. Check NSE's terms of service before use.

## 📝 License

MIT

## 🤝 Contributing

Feel free to submit issues and pull requests.

---

**Made with ❤️ for NSE data enthusiasts**

