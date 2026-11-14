import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
REGION = os.getenv("REGION", "africa")


class Country:
    """Stores and organizes the data of a single country."""

    def __init__(self, name, capital, region, population, area, languages, currencies):
        self.name = name
        self.capital = capital
        self.region = region
        self.population = population
        self.area = area
        self.languages = languages
        self.currencies = currencies

    @classmethod
    def from_json(cls, data):
        """Build a Country from one record of the v5 response."""
        capitals = data.get("capitals") or []
        return cls(
            name=(data.get("names") or {}).get("common", "N/A"),
            capital=capitals[0].get("name", "N/A") if capitals else "N/A",
            region=data.get("region", "N/A"),
            population=data.get("population") or 0,
            area=(data.get("area") or {}).get("kilometers") or 0,
            languages=[l.get("name", "?") for l in (data.get("languages") or [])],
            currencies=[c.get("name", "?") for c in (data.get("currencies") or [])],
        )

    @property
    def density(self):
        return self.population / self.area if self.area else 0

    def __str__(self):
        return (f"{self.name:<25}{self.capital:<20}"
                f"{self.population:>14,}{self.density:>10.1f}")


def fetch_countries(region):
    """Fetch every country in a region, following pagination."""
    url = f"{API_BASE_URL}/region/{region}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    fields = ("names.common,capitals,region,population,"
              "area.kilometers,languages,currencies")

    results, offset = [], 0
    while True:
        params = {"response_fields": fields, "limit": 100, "offset": offset}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        body = response.json()

        data = body.get("data")
        if not data:
            raise ValueError(f"Unexpected API response: {body}")

        results.extend(data["objects"])
        if not data["meta"].get("more"):
            break
        offset += 100
    return results


def display_summary(countries, top=10):
    countries = sorted(countries, key=lambda c: c.population, reverse=True)
    total = sum(c.population for c in countries)

    print("=" * 70)
    print(f"  COUNTRY SUMMARY - REGION: {REGION.upper()}")
    print("=" * 70)
    print(f"{'Country':<25}{'Capital':<20}{'Population':>14}{'Per km²':>10}")
    print("-" * 70)
    for c in countries[:top]:
        print(c)
    print("-" * 70)
    print(f"Countries in region : {len(countries)}")
    print(f"Total population    : {total:,}")

    largest = max(countries, key=lambda c: c.area)
    print(f"Largest by area     : {largest.name} ({largest.area:,.0f} km²)")
    top_country = countries[0]
    print(f"Most populous       : {top_country.name} | "
          f"Currencies: {', '.join(top_country.currencies) or 'N/A'} | "
          f"Languages: {', '.join(top_country.languages) or 'N/A'}")


def main():
    if not API_BASE_URL or not API_KEY:
        raise SystemExit("API_BASE_URL or API_KEY is missing. Check your .env file.")
    try:
        raw = fetch_countries(REGION)
        if not raw:
            raise SystemExit(f"No countries found for region '{REGION}'.")
        countries = [Country.from_json(item) for item in raw]
        display_summary(countries)
    except (requests.RequestException, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()