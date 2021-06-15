from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi

from datetime import datetime, timedelta


def testing(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    fields = {
        InstagramInsightsResult.Field.id,
        InstagramInsightsResult.Field.title,
        InstagramInsightsResult.Field.period,
        InstagramInsightsResult.Field.values
    }

    try:
        params = {
            "metric": [
                InstagramInsightsResult.Metric.impressions,
                InstagramInsightsResult.Metric.reach,
                InstagramInsightsResult.Metric.engagement,
                InstagramInsightsResult.Metric.saved,
                InstagramInsightsResult.Metric.video_views
            ],
            "period": [
                InstagramInsightsResult.Period.lifetime
            ]
        }

        data = IGMedia(fb_obj_id).get_insights(params=params, fields=fields)
    except:
        params = {
            "metric": [
                InstagramInsightsResult.Metric.impressions,
                InstagramInsightsResult.Metric.reach,
                InstagramInsightsResult.Metric.engagement,
                InstagramInsightsResult.Metric.saved
            ],
            "period": [
                InstagramInsightsResult.Period.lifetime
            ]
        }

        data = IGMedia(fb_obj_id).get_insights(params=params, fields=fields)

    try:
        video_views = data[4]["values"][0].get("value")
    except:
        video_views = 0

    output = {
        "impressions": data[0]["values"][0].get("value") or 0,
        "reach": data[1]["values"][0].get("value") or 0,
        "engagement": data[2]["values"][0].get("value") or 0,
        "saved": data[3]["values"][0].get("value") or 0,
        "video_views": video_views
    }

    return output


obj_id = '17855288603533239'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
access_token = 'EAAFZAzWeB7YsBAKrEmLdZAjBrotzZA5JZAxF23R6bQQ55ZByh0obnabCLKeKsJGeJ4r8dLnFeirICSwRZCZCfuMmT4BEiNk5wrKnenJJwZCUOsaTz46jYIabsBmb3rXR33SttPRRGvD4aalfMXZAGdbyEZCjQFxtwfBcD7eZA9PXis91ih6WuiXjFk0tfZCvWv02QmEZD'

print(testing(obj_id, app_id, app_secret, access_token))
