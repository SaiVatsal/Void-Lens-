# API Reference

## REST Endpoints

### `GET /`
Health check. Returns service name, version, and status.

### `POST /scan/username`
Scan a username across all registered modules.

**Request:**
```json
{
  "query": "johndoe",
  "categories": ["developer", "social"],
  "modules": null,
  "concurrency": 100,
  "timeout": 5
}
```

**Response:**
```json
{
  "query": "johndoe",
  "type": "username",
  "elapsed_seconds": 2.5,
  "total": 15,
  "found": 8,
  "not_found": 5,
  "unknown": 1,
  "errors": 1,
  "results": [
    {
      "site": "GitHub",
      "status": "Found",
      "url": "https://github.com/johndoe",
      "category": "Developer"
    }
  ]
}
```

### `POST /scan/email`
Same schema as username scan but for email addresses.

## Running the API

```bash
pip install voidlens[api]
uvicorn voidlens.api:app --host 0.0.0.0 --port 8000
```

Or with Docker:
```bash
docker-compose up -d
```
