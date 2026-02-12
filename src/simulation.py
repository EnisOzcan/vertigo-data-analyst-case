import numpy as np


def simulate_dau(retention_curve, daily_installs=20000, num_days=30):
    """
    Cohort-based DAU simulation.

    retention_curve: array-like of length >= num_days
        retention_curve[d-1] = probability a user is active on day d (D1..Dn)
    daily_installs: int
        new users acquired each day
    num_days: int
        number of days to simulate

    Returns
    -------
    dau: np.ndarray shape (num_days,)
        daily active users
    cohort_matrix: np.ndarray shape (num_days, num_days)
        cohort_matrix[t, k] = active users on day t coming from cohort k (k=0 is day1 cohort)
    """
    r = np.asarray(retention_curve, dtype=float)[:num_days]
    cohort_matrix = np.zeros((num_days, num_days), dtype=float)

    # cohort k arrives on day k (0-indexed)
    for k in range(num_days):
        # on day t >= k, cohort age is (t-k)+1 => retention index is (t-k)
        for t in range(k, num_days):
            cohort_matrix[t, k] = daily_installs * r[t - k]

    dau = cohort_matrix.sum(axis=1)
    return dau, cohort_matrix

def apply_sale(dau, base_purchase_rate, ecpm, ad_impressions,
               sale_start=15, sale_length=10):
  
    sale_end = sale_start + sale_length - 1
    daily_rev = []

    for idx in range(len(dau)):
        day = idx + 1
        pr = base_purchase_rate + (0.01 if sale_start <= day <= sale_end else 0.0)
        iap = dau[idx] * pr
        ads = dau[idx] * ad_impressions * (ecpm / 1000.0)
        daily_rev.append(iap + ads)

    return np.array(daily_rev)

def simulate_mixed_dau(ret_old, ret_new,
                       switch_day=20,
                       total_days=90,
                       installs_before=20000,
                       installs_old_after=12000,
                       installs_new_after=8000):

    

    ret_old = np.asarray(ret_old, dtype=float)[:total_days]
    ret_new = np.asarray(ret_new, dtype=float)[:total_days]

    dau = np.zeros(total_days, dtype=float)

    for t in range(total_days):
        for k in range(t + 1):
            age = t - k + 1

            if k < switch_day - 1:
                dau[t] += installs_before * ret_old[age - 1]
            else:
                dau[t] += installs_old_after * ret_old[age - 1]
                dau[t] += installs_new_after * ret_new[age - 1]

    return dau