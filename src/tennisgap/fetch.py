"""Download career JS files (the only code that touches the network)."""
import requests

from .errors import PlayerNotFoundError

BASE_URL = "https://www.tennisabstract.com/jsmatches/{slug}Career.js"
HEADERS = {"User-Agent": "Mozilla/5.0 (tennisgap package)"}


def fetch_career_js(slug, timeout=15):
    """Return the raw text of a player's career JS file."""
    url = BASE_URL.format(slug=slug)
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    if response.status_code == 404:
        raise PlayerNotFoundError(
            f"No player found for '{slug}'. Check the spelling of the name."
        )
    response.raise_for_status()
    return response.text
    