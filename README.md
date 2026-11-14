# Tennis abstract pulling/graphing package

This package downloads players match data from [tennisabstract.com](https://www.tennisabstract.com) and draws a scatter plot in the style of the NYT
visualization from HW2: the player's age on the x-axis. 

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-thevindu0.git
```

For development (includes `pytest`):

```bash
git clone https://github.com/UCB-stat159-f26/hw03-thevindu0.git
cd hw03-thevindu0
pip install -e ".[test]"
```

## Usage

```python
from tennisgap import get_player_matches, plot_age_gap

# Serena Williams data and plot
serena = get_player_matches("serena williams")
plot_age_gap(serena)

# Rafael Nadal data and plot
rafa = get_player_matches("Rafael Nadal")
plot_age_gap(rafa)

# Raises a meaningful error for unknown players
get_player_matches("GastonSanchez") gives an error message in all read and reads PlayerNotFoundError
```

Names are flexible: `"serena williams"`, `"Serena Williams"` and `"SerenaWilliams"` all work with the use of regex. 

## Public functions

| Function | Input | Output |
|---|---|---|
| `get_player_matches(name)` | player name (string) | `pandas.DataFrame` with columns `date`, `result`, `opponent`, `player_age`, `opponent_age`, `age_diff` |
| `plot_age_gap(matches)` | DataFrame from `get_player_matches()` | matplotlib `Figure` (scatter plot) |

`age_diff` is `player_age - opponent_age`.

## How it works

1. `names.py` normalizes the name into the site's format (`SerenaWilliams`).
2. `fetch.py` downloads the player's `...Career.js` file and the player's date of birth. If the player
   is not found, it raises `PlayerNotFoundError`.
3. `parse.py` extracts the `morematchmx` array from the JavaScript and builds the data frame.
   Women's files store the opponent's **date of birth**, so the age is derived from the match date.
   Men's files already store the opponent's **age**.
4. `api.py` exposes the two public functions and draws the plot.

```
tennis_abrsact_scripts
├── __init__.py
├── api.py      # public functions
├── errors.py   # PlayerNotFoundError
├── fetch.py    # network access (private helpers)
├── names.py    # name normalization
└── parse.py    # JS parsing and age calculations
tests/
├── test_fetch.py
└── test_parse.py
```

## Tests

```bash
pytest
```

Tests never contact the live server. The parsing tests use short mock excerpts of a female and a male
career JS file, and the error test replaces the network call with a stub.

## Reflections

- **Git and nested repositories.** When I was first starting the project, I had so many nested folders within each other when I was trying to get organized with the project.
  This led to a major headache, to the point where my files were not staged and never went into GitHub, and when I tried to push, it kept saying that there was nothing to commit.
  It got so bad that I just deleted all the files and started from scratch, so that's why my instructions file is missing. I have mostly been using git status for all
  my projects, but for whatever reason I stopped using it in my first attempt, which is not a mistake; I will do it again.  
  listed.
- **Small commits.** Committing one module at a time made my history readable, but it was very hard to force myself to do. But it does make my work very readable, and I see the benefit of it. 
- **Testing in Git Ignore** I had a lot of fun with my scripts just checking what the graphs look like for different players. I had my roommate, who played tennis in high school, play with it and
  look into all his favorite players.
- **What I'd improve.** I think my plot generation could be improved, and my file nesting could be improved if I learned more about it. 

AI disclosure: I used Claude Sonnet 5.5 for coding, debugging, and a quick fix for my read me. 
