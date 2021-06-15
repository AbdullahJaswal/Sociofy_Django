from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi

from celery import shared_task


@shared_task
def post_analytics(obj_id, app_id, app_secret, access_token):
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

        data = IGMedia(obj_id).get_insights(params=params, fields=fields)
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

        data = IGMedia(obj_id).get_insights(params=params, fields=fields)

    try:
        video_views = data[4]["values"][0].get("value")
    except:
        video_views = 0

    output = {
        "post_id": obj_id,
        "impressions": data[0]["values"][0].get("value") or 0,
        "reach": data[1]["values"][0].get("value") or 0,
        "engagement": data[2]["values"][0].get("value") or 0,
        "saved": data[3]["values"][0].get("value") or 0,
        "video_views": video_views
    }

    return output
