import numpy as np
from scipy.optimize import curve_fit


def exp_decay(day, a, b):
    return a * np.exp(-b * (day - 1))


def fit_retention_curve(retention_points, max_day=30):
    days = np.array(list(retention_points.keys()))
    values = np.array(list(retention_points.values()))

    params, _ = curve_fit(exp_decay, days, values, bounds=(0, 1))
    a, b = params

    all_days = np.arange(1, max_day + 1)
    fitted_retention = exp_decay(all_days, a, b)

    return all_days, fitted_retention, (a, b)


def retention_new_A(days):
    return 0.58 * np.exp(-0.12 * (days - 1))

def retention_new_B(days):
    return 0.52 * np.exp(-0.10 * (days - 1))


    