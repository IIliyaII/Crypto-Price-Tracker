import os
import sys
from doctest import master

import requests

BASE_URL = "https://api.freecryptoapi.com/v1"



def get_auth_headers():
    api_key = os.getenv("COINCAP_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "❌ API key not found.\n"
            "Set the environment variable:\n"
            "export COINCAP_API_KEY='your_key_here'"
        )

    return {
        "Authorization": f"Bearer {api_key}"
    }


def fetch_asset_data(symbol: str) -> dict:
    headers = get_auth_headers()
    url = f"{BASE_URL}/getData?symbol={symbol.upper()}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        raise SystemExit(
            "❌ Connection error: check your internet connection."
        )

    except requests.exceptions.Timeout:
        raise SystemExit(
            "❌ Request timed out: the server did not respond. Try again."
        )

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code

        if status == 404:
            raise SystemExit(
                f"❌ Asset '{symbol}' not found. Check the symbol (e.g. bitcoin)"
            )

        elif status == 401:
            raise SystemExit(
                "❌ Invalid API key. Please check your credentials."
            )

        else:
            raise SystemExit(f"❌ HTTP error {status}: {e}")

    except requests.exceptions.RequestException as e:
        raise SystemExit(f"❌ Network error: {e}")


def parse_asset_info(data: dict, symbol: str) -> dict:
    try:
        asset = data["data"]

        return {
            "name": asset.get("name", symbol),
            "symbol": asset.get("symbol", symbol.upper()),
            "price": float(asset["priceUsd"]),
            "change_24h": float(asset.get("changePercent24Hr", 0)),
        }

    except (KeyError, ValueError, TypeError):
        raise SystemExit(
            "❌ Unexpected API response format. The API may have changed."
        )


def display_price(info: dict):
    change = info["change_24h"]

    arrow = "▲" if change >= 0 else "▼"
    sign = "+" if change >= 0 else ""

    print(f"\n{'─' * 35}")
    print(f" {info['name']} ({info['symbol']})")
    print(f" Price: ${info['price']:,.2f} USD")
    print(f" 24h Change: {arrow} {sign}{change:.2f}%")
    print(f"{'─' * 35}\n")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "❌ Usage:\n"
            "python main.py <symbol>\n"
            "Example: python main.py bitcoin"
        )

    symbol = sys.argv[1]

    print(f"🔍 Fetching price for {symbol.upper()}...")

    raw_data = fetch_asset_data(symbol)
    asset_info = parse_asset_info(raw_data, symbol)

    display_price(asset_info)


if __name__ == "__main__":
    main()

