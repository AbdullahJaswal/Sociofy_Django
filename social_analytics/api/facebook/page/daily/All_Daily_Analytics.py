from facebook_business.api import FacebookAdsApi

from facebook_business.adobjects.page import Page
from facebook_business.adobjects.insightsresult import InsightsResult

from datetime import datetime, timedelta


def all_daily_analytics(obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    until = datetime.today()
    since = until - timedelta(days=93)

    params = {
        "metric": [
            "page_impressions",
            "page_impressions_unique",
            "page_fan_adds",
            "page_call_phone_clicks_logged_in_unique",
            "page_get_directions_clicks_logged_in_unique",
            "page_website_clicks_logged_in_unique",
            "page_views_total"
        ],
        "period": InsightsResult.Period.day,
        "since": since.strftime('%Y-%m-%d'),
        "until": until.strftime('%Y-%m-%d')
    }

    fields = {
        InsightsResult.Field.id,
        InsightsResult.Field.title,
        InsightsResult.Field.period,
        InsightsResult.Field.values
    }

    return Page(obj_id).get_insights(params=params, fields=fields)