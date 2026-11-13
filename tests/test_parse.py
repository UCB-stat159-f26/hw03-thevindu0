import pandas as pd
import pytest
from tennisgap.names import normalize_name
from tennisgap.parse import build_matches, extract_rows, opponent_age

FEMALE_JS = '''# female
var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0"],
  ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0"]]'''

MALE_JS = '''# male
var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0"],
  ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0"]]'''


def test_extract_rows_counts_matches():
    assert len(extract_rows(FEMALE_JS)) == 2


def test_extract_rows_without_array_raises():
    with pytest.raises(ValueError):
        extract_rows("var other = [];")


def test_female_opponent_age_from_dob():
    age = opponent_age(pd.Timestamp("1995-10-30"), "19770119")
    assert age == pytest.approx(18.78, abs=0.01)


def test_male_opponent_age_passthrough():
    assert opponent_age(pd.Timestamp("2001-09-10"), "22.26") == 22.26


def test_build_matches_female_columns_and_result():
    df = build_matches(FEMALE_JS, "19811005")
    assert {"player_age", "opponent_age", "age_diff", "result"} <= set(df.columns)
    assert df["result"].tolist() == ["L", "L"]
    assert df["player_age"].iloc[0] == pytest.approx(14.07, abs=0.02)


def test_build_matches_male_uses_given_age():
    df = build_matches(MALE_JS, "19830101")
    assert df["opponent_age"].iloc[0] == pytest.approx(22.264, abs=1e-3)
    assert df["result"].tolist() == ["L", "W"]


@pytest.mark.parametrize("raw", ["serena williams", "Serena Williams", "SerenaWilliams"])
def test_normalize_name_variants(raw):
    assert normalize_name(raw) == "SerenaWilliams"


def test_normalize_name_rejects_empty():
    with pytest.raises(ValueError):
        normalize_name("  ")
