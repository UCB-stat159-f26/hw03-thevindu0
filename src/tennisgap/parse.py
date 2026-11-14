import json
import re
import pandas as pd

DATE_FMT = "%Y%m%d"
IDX_DATE, IDX_RESULT, IDX_OPPONENT, IDX_OPP_AGE_OR_DOB = 0, 4, 11, 16


def extract_rows(js_text):
    found = re.search(r"var\s+morematchmx\s*=\s*(\[.*\])", js_text, re.S)
    if not found:
        raise ValueError("No 'morematchmx' array found in JS content.")
    return json.loads(found.group(1))


def years_between(start, end):
    return (end - start) / pd.Timedelta(days=365.25)


def opponent_age(match_date, raw_value):
    "Women's files give opponent DOB (YYYYMMDD); and gets men's age directly."
    raw = str(raw_value)
    if re.fullmatch(r"\d{8}", raw):
        return years_between(pd.to_datetime(raw, format=DATE_FMT), match_date)
    return float(raw) if raw else float("nan")


def rows_to_frame(rows):
    return pd.DataFrame({
        "date": pd.to_datetime([r[IDX_DATE] for r in rows], format=DATE_FMT),
        "result": [r[IDX_RESULT] for r in rows],
        "opponent": [r[IDX_OPPONENT] for r in rows],
        "opp_raw": [r[IDX_OPP_AGE_OR_DOB] for r in rows],
    })


def add_ages(frame, player_dob):
    dob = pd.to_datetime(player_dob, format=DATE_FMT)
    out = frame.copy()
    out["player_age"] = years_between(dob, out["date"])
    out["opponent_age"] = [opponent_age(d, r) for d, r in zip(out["date"], out["opp_raw"])]
    out["age_diff"] = out["player_age"] - out["opponent_age"]
    return out.drop(columns="opp_raw").dropna(subset=["opponent_age"])


def build_matches(js_text, player_dob):
    return add_ages(rows_to_frame(extract_rows(js_text)), player_dob)
