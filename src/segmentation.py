import pandas as pd

def first_day_user_table(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate D0 metrics per user for segmentation."""
    d0 = df[df["days_since_install"] == 0].copy()
    agg = d0.groupby("user_id", as_index=False).agg(
        platform=("platform", "first"),
        country=("country", "first"),
        d0_sessions=("total_session_count", "sum"),
        d0_duration=("total_session_duration", "sum"),
        d0_avg_session=("avg_session_duration", "mean"),
        d0_matches=("match_end_count", "sum"),
        d0_victory_rate=("victory_rate", "mean"),
        d0_total_revenue=("total_revenue", "sum"),
        d0_iap=("iap_revenue", "sum"),
        d0_ad=("ad_revenue", "sum"),
    )
    return agg

def segment_first_day(users: pd.DataFrame) -> pd.DataFrame:
    """Rule-based segments that read well in README."""
    u = users.copy()

    # quantile thresholds
    q_dur = u["d0_duration"].quantile(0.75)
    q_sess = u["d0_sessions"].quantile(0.75)

    def label(r):
        if r["d0_sessions"] <= 1 and r["d0_duration"] <= 60:
            return "Early Drop-off Risk"
        if r["d0_duration"] >= q_dur and r["d0_sessions"] >= q_sess:
            return "Highly Engaged"
        if r["d0_matches"] >= 5 and r["d0_victory_rate"] >= 0.6:
            return "Competitive Winners"
        return "Casual"

    u["segment"] = u.apply(label, axis=1)
    return u
