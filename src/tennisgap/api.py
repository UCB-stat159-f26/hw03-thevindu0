import matplotlib.pyplot as plt
from .fetch import fetch_career_js, fetch_player_dob
from .names import normalize_name
from .parse import build_matches

COLORS = {"W": "#2a9d8f", "L": "#e76f51"}


def get_player_matches(name):
    """Return a tidy DataFrame of a player's career matches with ages."""
    slug = normalize_name(name)
    return build_matches(fetch_career_js(slug), fetch_player_dob(slug))


def plot_age_gap(matches):
    """Scatter: player age (x) vs. player minus opponent age (y), colored by W/L."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for result, grp in matches.groupby("result"):
        ax.scatter(grp["player_age"], grp["age_diff"], s=12, alpha=0.7,
                   color=COLORS.get(result, "gray"), label=result)
    ax.axhline(0, color="black", lw=0.8)
    ax.set(xlabel="Player age", ylabel="Player age minus opponent age")
    ax.legend(title="Result")
    return fig
