# Deployment Guide

## 🚀 Deploy to Railway

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize Project
```bash
railway init
```

### Step 4: Deploy
```bash
railway up
```

### Step 5: Get Your URL
```bash
railway domain
```

Your API will be available at: `https://your-app.railway.app`

---

## 🐳 Local Docker Testing

### Build and Run
```bash
docker-compose up --build
```

### Access API
- API: http://localhost:5000
- Health: http://localhost:5000/health

### Stop
```bash
docker-compose down
```

---

## 📊 API Endpoints (After Deployment)

Replace `localhost:5000` with your Railway URL:

```bash
# Health check
curl https://your-app.railway.app/health

# Event Calendar
curl https://your-app.railway.app/event-calendar?page=1&per_page=50

# Announcements
curl https://your-app.railway.app/announcements?market=equity

# CRD
curl https://your-app.railway.app/crd

# Credit Rating
curl https://your-app.railway.app/credit-rating?market=equity
```

---

## ⚙️ Environment Variables (Optional)

In Railway dashboard, you can set:
- `PORT` - API port (default: 5000)
- `PYTHONUNBUFFERED` - Set to 1 for logging

---

## 📝 Notes

- All 4 monitors run automatically every 5 minutes
- Data is stored in memory (containers)
- First scrape happens on startup (may take 1-2 minutes)
- API starts after monitors create initial data
- Chrome runs in headless mode

---

## 🔍 Monitoring

Check logs in Railway dashboard:
- Monitor scraping activity
- API requests
- Any errors

---

## 💰 Railway Pricing

- Free tier: 500 hours/month
- Paid: $5/month for unlimited
- Each deployment uses 1 service

---

## 🛠️ Troubleshooting

### API returns 404 for data endpoints
- Wait 1-2 minutes after deployment
- Monitors need time to scrape initial data
- Check `/health` endpoint

### Memory issues
- Railway free tier: 512MB RAM
- May need paid plan for all 4 monitors
- Consider running fewer monitors

### Chrome crashes
- Headless mode is enabled
- Should work on Railway
- Check logs for errors

---

## 📱 Quick Deploy (One Command)

```bash
# Clone, login, and deploy
git clone <your-repo>
cd EventScrapeAPI
railway login
railway init
railway up
```

Done! 🎉

