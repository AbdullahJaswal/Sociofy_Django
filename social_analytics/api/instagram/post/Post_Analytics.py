from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi


def post_analytics(fb_obj_id, app_id, app_secret, access_token):
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

        return IGMedia(fb_obj_id).get_insights(params=params, fields=fields)
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

        return IGMedia(fb_obj_id).get_insights(params=params, fields=fields)
