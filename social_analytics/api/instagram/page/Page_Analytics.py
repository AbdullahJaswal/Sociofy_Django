from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi


def page_analytics(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    params = {
        "metric": [
            "impressions",
            "reach",
            "follower_count",
            "email_contacts",
            "phone_call_clicks",
            "text_message_clicks",
            "get_directions_clicks",
            "website_clicks",
            "profile_views"
        ],
        "period": [
            InstagramInsightsResult.Period.day
        ]
    }

    fields = {
        InstagramInsightsResult.Field.id,
        InstagramInsightsResult.Field.title,
        InstagramInsightsResult.Field.period,
        InstagramInsightsResult.Field.values
    }

    return IGUser(fb_obj_id).get_insights(params=params, fields=fields)
