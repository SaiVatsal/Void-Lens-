# VoidLens — Usage & Free Deployment Guide

> *Peer into the digital void.*

---

## 1. Installation

```bash
# Clone
git clone https://github.com/your-username/voidlens.git
cd voidlens

# Install
pip install -e .

# With API + dev tools
pip install -e ".[all]"
```

---

## 2. CLI Usage

### Single Username Scan
```bash
voidlens scan -u johndoe
```

### Single Email Scan
```bash
voidlens scan -e test@gmail.com
```

### Both at Once
```bash
voidlens scan -u johndoe -e test@gmail.com
```

### Bulk Scan from File
```bash
# Create a file with one entry per line
echo "johndoe" > usernames.txt
echo "janedoe" >> usernames.txt

voidlens scan -uf usernames.txt
voidlens scan -ef emails.txt
```

### Filter by Category
```bash
voidlens scan -u johndoe -c developer
voidlens scan -u johndoe -c gaming -c social
```

### Run Specific Modules Only
```bash
voidlens scan -u johndoe -m github -m reddit -m steam
```

### Verbose Mode (shows URL, response time, status code)
```bash
voidlens scan -u johndoe -v
```

### Export Reports
```bash
voidlens scan -u johndoe --json report.json
voidlens scan -u johndoe --csv report.csv
voidlens scan -u johndoe --html report.html
voidlens scan -u johndoe --md report.md
voidlens scan -u johndoe --xml report.xml
voidlens scan -u johndoe --sarif report.sarif

# Multiple exports at once
voidlens scan -u johndoe --json report.json --html report.html --csv report.csv
```

### With Proxy
```bash
# Create proxies.txt with one proxy per line:
# http://127.0.0.1:8080
# socks5://127.0.0.1:1080

voidlens scan -u johndoe -P proxies.txt
```

### Tune Performance
```bash
voidlens scan -u johndoe --concurrency 50 --timeout 10
```

---

## 3. Library Mode (Python)

```python
import asyncio
from voidlens import scan_username, scan_email

async def main():
    # Scan username
    result = await scan_username("johndoe")
    for site in result.results:
        print(f"{site.site}: {site.status.value}")

    # Scan email
    result = await scan_email("test@gmail.com")
    for site in result.results:
        print(f"{site.site}: {site.status.value}")

asyncio.run(main())
```

### With Filters
```python
result = await scan_username(
    "johndoe",
    categories=["developer", "gaming"],
    concurrency=50,
    timeout=10,
)
```

---

## 4. API Mode

### Start the API
```bash
pip install voidlens[api]
uvicorn voidlens.api:app --host 0.0.0.0 --port 8000
```

### Scan Username
```bash
curl -X POST http://localhost:8000/scan/username \
  -H "Content-Type: application/json" \
  -d '{"query": "johndoe"}'
```

### Scan Email
```bash
curl -X POST http://localhost:8000/scan/email \
  -H "Content-Type: application/json" \
  -d '{"query": "test@gmail.com"}'
```

### API Docs (auto-generated)
Open `http://localhost:8000/docs` in your browser.

---

## 5. Deploy for FREE

### Option A: Railway.app (Easiest)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → Sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your `voidlens` repo
5. Railway auto-detects the `Dockerfile`
6. Set **Port** = `8000` in Settings → Networking
7. Done — you get a free public URL

**Free tier:** 500 hours/month, 512 MB RAM

---

### Option B: Render.com

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → **Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -e ".[api]"`
   - **Start Command:** `uvicorn voidlens.api:app --host 0.0.0.0 --port $PORT`
5. Deploy — free `.onrender.com` URL

**Free tier:** 750 hours/month, spins down after 15 min inactivity

---

### Option C: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch (uses Dockerfile)
cd voidlens
fly launch

# Deploy
fly deploy
```

**Free tier:** 3 shared VMs, 256 MB RAM each

---

### Option D: Koyeb.com

1. Push code to GitHub
2. Go to [koyeb.com](https://koyeb.com) → Create App
3. Select GitHub repo → Docker deployment
4. Set port = `8000`
5. Deploy

**Free tier:** 1 nano instance, always-on

---

### Option E: Vercel (Serverless — API only)

1. Create `api/index.py`:
```python
from voidlens.api import app
# Vercel auto-detects FastAPI
```

2. Create `vercel.json`:
```json
{
  "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "api/index.py"}]
}
```

3. Deploy:
```bash
npm i -g vercel
vercel
```

**Free tier:** 100 GB bandwidth, serverless

---

### Option F: GitHub Codespaces (Dev/Testing)

1. Open your repo on GitHub
2. Click **Code** → **Codespaces** → **Create**
3. In the terminal:
```bash
pip install -e ".[all]"
voidlens scan -u johndoe
```

**Free tier:** 120 core-hours/month

---

### Option G: Google Cloud Run (Generous Free Tier)

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/voidlens

# Deploy
gcloud run deploy voidlens \
  --image gcr.io/YOUR_PROJECT/voidlens \
  --platform managed \
  --allow-unauthenticated \
  --port 8000
```

**Free tier:** 2 million requests/month, 360K GB-seconds

---

## 6. Quick Reference

| Command | Description |
|---|---|
| `voidlens scan -u USER` | Scan username |
| `voidlens scan -e EMAIL` | Scan email |
| `voidlens scan -uf FILE` | Bulk username scan |
| `voidlens scan -ef FILE` | Bulk email scan |
| `voidlens scan -v` | Verbose output |
| `voidlens scan -c CATEGORY` | Filter by category |
| `voidlens scan -m MODULE` | Run specific module |
| `voidlens scan -P FILE` | Use proxy list |
| `voidlens scan --json FILE` | Export JSON |
| `voidlens scan --csv FILE` | Export CSV |
| `voidlens scan --html FILE` | Export HTML |
| `voidlens version` | Show version |
| `voidlens update` | Check for updates |

---

## 7. Available Categories

`developer` · `social` · `forums` · `streaming` · `gaming` · `shopping` · `programming` · `finance` · `cloud` · `music` · `education` · `productivity` · `security` · `open source` · `ai` · `business` · `blogging` · `photography` · `art` · `video` · `crypto`

---

## 8. Config File

Edit `config/config.yaml` to customize defaults:

```yaml
timeout: 5
concurrency: 100
retries: 3
cache_enabled: true
cache_ttl: 3600

proxy:
  enabled: false
  file: config/proxies.yaml
  rotate: true
```

---

*Built with precision. Deployed for free. Peer into the void.* ◈
