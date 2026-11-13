import pytest
from tennisgap import fetch
from tennisgap.errors import PlayerNotFoundError


def test_unknown_player_raises_clear_error(monkeypatch):
    monkeypatch.setattr(fetch, "_get", lambda url: None)  # no network
    with pytest.raises(PlayerNotFoundError, match="not found"):
        fetch.fetch_career_js("GastonSanchez")
