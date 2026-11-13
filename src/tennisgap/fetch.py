import re
import requests
from .errors import PlayerNotFoundError

BASE = "https://www.tennisabstract.com"
HEADERS = {"User-Agent": "tennisgap (course project)"}
# I am making an assumption here that the player's DOB appears in the site.
PLAYER_PAGES = ["/cgi-bin/wplayer.cgi?p={}", "/cgi-bin/player.cgi?p={}"]


def _get(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    return resp.text if resp.status_code == 200 else None


def fetch_career_js(slug):
    text = _get(f"{BASE}/jsmatches/{slug}Career.js")
    if text is None or "morematchmx" not in text:
        raise PlayerNotFoundError(
            f"Player '{slug}' not found on tennisabstract.com. "
            "Please check the spelling, e.g. 'Serena Williams'."
        )
    return text


def fetch_player_dob(slug):
    for page in PLAYER_PAGES:
        text = _get(BASE + page.format(slug)) or ""
        found = re.search(r"dob\s*=\s*(\d{8})", text)
        if found:
            return found.group(1)
    raise PlayerNotFoundError(f"Could not find date of birth for '{slug}'.")
