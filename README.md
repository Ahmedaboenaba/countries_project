# 🌍 Countries Summary: REST API Client in Python

A small Python program that connects to the **REST Countries API (v5)**, retrieves country data as JSON, parses it into a custom `Country` class, and prints a clear, formatted summary for a chosen region.

---

## ✨ Features

- Authenticated requests to a public REST API using an API key
- JSON parsing of nested objects and lists, with safe handling of missing fields
- A `Country` class that stores and organizes each record
- Automatic pagination, so the full region is always retrieved
- A formatted console report: top countries by population, totals, largest country, and more
- Secrets kept out of the code via a `.env` file
- Runs inside an isolated Python virtual environment

---

## ✅ Requirements Checklist

| # | Requirement | How it is met |
|---|-------------|---------------|
| 1 | API integration | `requests` calls `https://api.restcountries.com/countries/v5` |
| 2 | JSON parsing | `response.json()` plus navigation of `data.objects` |
| 3 | Class implementation | `Country` class with `from_json()`, `density`, and `__str__()` |
| 4 | Formatted output | `display_summary()` prints an aligned table and statistics |
| 5 | Virtual environment | Project runs inside `venv` |
| 6 | Environment variables | API key and settings loaded from `.env` with `python-dotenv` |

---

## 📁 Project Structure

```
countries_project/
├── main.py            # Application code
├── requirements.txt   # Python dependencies
├── .env               # Real API key (NEVER share or commit)
├── .env.example       # Safe template with no secrets
├── .gitignore         # Keeps .env and venv out of Git
└── README.md          # This file
```

---

## 🚀 Setup and Installation

### Step 1: Get an API key

REST Countries v5 requires a key on every request.

1. Sign up at [restcountries.com/sign-up](https://restcountries.com/sign-up).
2. Create a key from your account's **API Keys** page.

### Step 2: Create and activate a virtual environment

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate.bat
# macOS / Linux
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

To create the file yourself from scratch:

```bash
pip install requests python-dotenv
pip freeze > requirements.txt
```

### Step 4: Configure environment variables

Copy the template and fill in your key:

```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```

Then edit `.env`:

```
API_BASE_URL=https://api.restcountries.com/countries/v5
API_KEY=your_real_api_key_here
REGION=Africa
```

> `API_BASE_URL` must contain **only the endpoint**, with no query string such as `?q=...`.
> Valid regions: `Africa`, `Americas`, `Asia`, `Europe`, `Oceania`.

### Step 5: Run the program

```bash
python main.py
```

---

## 🔍 How It Works

### 1. API integration

The key is read from the environment and sent in the `Authorization` header:

```python
headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get(url, headers=headers, params=params, timeout=10)
response.raise_for_status()
```

`raise_for_status()` stops the program on HTTP errors such as `401 Unauthorized`.

### 2. JSON parsing

```python
body = response.json()          # JSON text -> Python dict/list
records = body["data"]["objects"]
```

The v5 response is nested:

```json
{
  "data": {
    "objects": [
      {
        "names": {"common": "Nigeria"},
        "capitals": [{"name": "Abuja"}],
        "population": 223800000,
        "area": {"kilometers": 923768},
        "languages": [{"name": "English"}],
        "currencies": [{"name": "Nigerian naira"}]
      }
    ],
    "meta": {"total": 60, "more": false}
  }
}
```

Missing or null fields are handled with `.get()` and fallbacks, so one incomplete record never crashes the program:

```python
capitals = data.get("capitals") or []
area = (data.get("area") or {}).get("kilometers") or 0
```

### 3. The `Country` class

Each JSON record becomes a `Country` object through the `from_json()` class method. The class also provides a computed `density` property (population per km²) and a `__str__()` method that formats one table row.

### 4. Pagination

The free plan returns at most 100 records per request. The program requests `limit=100` and follows `meta.more` with an increasing `offset` until every record has been retrieved.

### 5. Formatted output

`display_summary()` sorts countries by population and prints the top 10 in an aligned table, followed by region totals.

---

## 📊 Sample Output

```
======================================================================
  COUNTRY SUMMARY - REGION: AFRICA
======================================================================
Country                  Capital                 Population   Per km²
----------------------------------------------------------------------
Nigeria                  Abuja                  223,800,000     242.3
DRC                      Kinshasa               116,452,000      49.7
Ethiopia                 Addis Ababa            111,652,998     101.1
Egypt                    Cairo                  108,613,296     108.3
Tanzania                 Dodoma                  70,038,850      74.1
South Africa             Pretoria                63,015,904      51.6
Kenya                    Nairobi                 54,227,015      93.4
Sudan                    Khartoum                53,282,719      28.3
Algeria                  Algiers                 47,400,000      19.9
Uganda                   Kampala                 45,905,417     190.0
----------------------------------------------------------------------
Countries in region : 60
Total population    : 1,489,812,112
Largest by area     : Algeria (2,381,741 km²)
Most populous       : Nigeria | Currencies: Nigerian naira | Languages: English
```

> The region count can be higher than the number of sovereign states because the API also includes dependencies and territories.

---

## 🔐 Security

- The real API key lives **only** in `.env`.
- `.env` is listed in `.gitignore`, so it is never committed.
- Share `.env.example` instead, which contains no secrets.
- If a key is ever exposed, revoke it from your REST Countries **API Keys** page and create a new one.

Contents of `.gitignore`:

```
.env
venv/
__pycache__/
```

---

## 🛠️ Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `AttributeError: 'str' object has no attribute 'get'` | API returned an error object instead of a list | Validate the response; check the URL and key |
| `401 Unauthorized` | Missing, wrong, or placeholder API key | Put a valid key in `.env` |
| `401` with a strange URL such as `...v5?q=canada/region/...` | `API_BASE_URL` contains a query string | Use `https://api.restcountries.com/countries/v5` only |
| `No countries found for region` | Demo key (`rc_live_demo`) returns only sample data, or the region name is wrong | Use a real key and a valid region |
| `403 Forbidden` | Account pending, or quota exceeded | Check your account on restcountries.com |

---

## 🧰 Tech Stack

- **Python 3**
- [`requests`](https://pypi.org/project/requests/): HTTP client
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): loads `.env` variables
- [REST Countries API v5](https://restcountries.com): data source

---

## 🔭 Possible Improvements

- Command-line arguments with `argparse` (for example `--region Europe --top 5`)
- Export results to CSV or JSON
- Filter to sovereign states only
- Unit tests for `Country.from_json()` using sample JSON

---

## 👤 Author

**[Your Name]**: Week 1 Project