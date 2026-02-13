import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # totals
    df["total_revenue"] = df["iap_revenue"] + df["ad_revenue"]

    # days since install (assumes event_date/install_date are parseable)
    event = pd.to_datetime(df["event_date"], errors="coerce")
    inst = pd.to_datetime(df["install_date"], errors="coerce")
    df["days_since_install"] = (event - inst).dt.days
    df["days_since_install"] = df["days_since_install"].fillna(0).clip(lower=0)

    # victory rate (avoid /0)
    denom = df["match_end_count"].replace(0, pd.NA)
    df["victory_rate"] = (df["victory_count"] / denom).fillna(0).clip(0, 1)

    # avg session duration per session (avoid /0)
    denom2 = df["total_session_count"].replace(0, pd.NA)
    df["avg_session_duration"] = (df["total_session_duration"] / denom2).fillna(0)

    # connection error per session (avoid /0)
    denom3 = df["total_session_count"].replace(0, pd.NA)
    df["conn_error_per_session"] = (df["server_connection_error"] / denom3).fillna(0)

    return df
