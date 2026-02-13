import pandas as pd

EXPECTED_COLS = [
    "user_id","event_date","platform","install_date","country",
    "total_session_count","total_session_duration",
    "match_start_count","match_end_count","victory_count","defeat_count",
    "iap_revenue","ad_revenue"
]

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Column check (soft)
    missing = set(EXPECTED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # Dates
    df["event_date"] = pd.to_datetime(df["event_date"]).dt.date
    df["install_date"] = pd.to_datetime(df["install_date"]).dt.date

    # Numeric safety
    num_cols = [
        "total_session_count","total_session_duration",
        "match_start_count","match_end_count","victory_count","defeat_count",
        "iap_revenue","ad_revenue"
    ]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # Basic guards
    df["match_end_count"] = df["match_end_count"].clip(lower=0)
    df["total_session_count"] = df["total_session_count"].clip(lower=0)
    df["total_session_duration"] = df["total_session_duration"].clip(lower=0)

    return df