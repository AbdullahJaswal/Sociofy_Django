from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi

from datetime import datetime, timedelta


def impressions_analytic(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    until = datetime.today()
    since = until - timedelta(days=30)

    params = {
        "metric": [
            "impressions"
        ],
        "period": [
            InstagramInsightsResult.Period.day
        ],
        "since": since.strftime('%Y-%m-%d'),
        "until": until.strftime('%Y-%m-%d')
    }

    fields = {
        InstagramInsightsResult.Field.id,
        InstagramInsightsResult.Field.title,
        InstagramInsightsResult.Field.period,
        InstagramInsightsResult.Field.values
    }

    return IGUser(fb_obj_id).get_insights(params=params, fields=fields)
