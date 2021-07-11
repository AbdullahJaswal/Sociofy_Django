import numpy as np
import pandas as pd
from scipy.stats import stats  # noqa. <-- Used to suppress error highlight.


def metrics_correlation(daily_analytics):
    df = pd.DataFrame(daily_analytics)

    df = df.drop(['id', 'pageID', 'datetime', 'page_id'], axis=1)

    df = df.dropna()

    df['follower_count'] = df['follower_count'].apply(int)

    columns = ["impressions", "reach", "follower_count", "profile_views"]

    df = df[columns]

    z_scores = stats.zscore(df)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 2).all(axis=1)
    new_df = df[filtered_entries]

    corr = new_df.corr(method="pearson")

    data = {
        "impressions_reach": round(corr['impressions']['reach'] * 100, 2),
        "impressions_follower_count": round(corr['impressions']['follower_count'] * 100, 2),
        "impression_profile_views": round(corr['impressions']['profile_views'] * 100, 2),
        "reach_follower_count": round(corr['reach']['follower_count'] * 100, 2),
        "reach_profile_views": round(corr['reach']['profile_views'] * 100, 2),
        "profile_views_follower_count": round(corr['profile_views']['follower_count'] * 100, 2)
    }

    return data
