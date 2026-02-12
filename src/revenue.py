import numpy as np


def compute_revenue(dau, purchase_rate, ecpm, ad_impressions_per_dau):
    """
    Revenue model (daily):

    IAP revenue (proxy): dau * purchase_rate
    Ad revenue: dau * ad_impressions_per_dau * (ecpm / 1000)

    Returns
    -------
    total: np.ndarray
    iap: np.ndarray
    ads: np.ndarray
    """
    dau = np.asarray(dau, dtype=float)

    iap = dau * float(purchase_rate)
    ads = dau * float(ad_impressions_per_dau) * (float(ecpm) / 1000.0)
    total = iap + ads
    return total, iap, ads


def cumulative(x):
    x = np.asarray(x, dtype=float)
    return np.cumsum(x)