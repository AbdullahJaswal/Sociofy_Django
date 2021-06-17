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

    until = datetime.today()
    since = until - timedelta(days=30)

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


obj_id = '17841431321059427'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
access_token = 'EAAFZAzWeB7YsBALoZAEhMGazhSDQtMYS0nfOKM8kNoSLq8FCowODn1vVU6mfSxwXDRssZBuT8pyg51FHaXqewTBhLGvOWG19cGfA8kMZBmFKJySZCwvuxoctnpXqBffWHZAnZA923BZCYsbLVE1Yb3dX3czPjzpgequCaPfwZAGXBWxlaulyy2rMZAjeNbeHTRWNoZD'

print(testing(obj_id, app_id, app_secret, access_token))
