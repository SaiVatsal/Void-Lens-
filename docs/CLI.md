# CLI Reference

## Usage

```bash
voidlens scan [OPTIONS]
```

## Options

| Flag | Short | Description |
|------|-------|-------------|
| `--username` | `-u` | Username to scan |
| `--email` | `-e` | Email to scan |
| `--username-file` | `-uf` | File with usernames (one per line) |
| `--email-file` | `-ef` | File with emails (one per line) |
| `--category` | `-c` | Filter by category (repeatable) |
| `--module` | `-m` | Run specific module (repeatable) |
| `--verbose` | `-v` | Show detailed output |
| `--concurrency` | | Max concurrent requests (default: 100) |
| `--timeout` | | Request timeout in seconds (default: 5) |
| `--proxy` | `-P` | Proxy list file |
| `--json` | | Export JSON report |
| `--csv` | | Export CSV report |
| `--html` | | Export HTML report |
| `--md` | | Export Markdown report |
| `--xml` | | Export XML report |
| `--sarif` | | Export SARIF report |

## Examples

```bash
# Single username scan
voidlens scan -u johndoe

# Single email scan
voidlens scan -e test@gmail.com

# Both simultaneously
voidlens scan -u johndoe -e test@gmail.com

# Bulk scan from file
voidlens scan -uf usernames.txt

# Filter by category
voidlens scan -u johndoe -c developer -c gaming

# Verbose + export
voidlens scan -u johndoe -v --json report.json --html report.html

# With proxy
voidlens scan -u johndoe -P proxies.txt
```

## Other Commands

```bash
voidlens version   # Show version
voidlens update    # Check for updates
```
