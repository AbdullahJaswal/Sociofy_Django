import json

from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi

from facebook_business.adobjects.page import Page
from facebook_business.adobjects.post import Post
from facebook_business.adobjects.insightsresult import InsightsResult

from datetime import datetime, timedelta

from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.api import FacebookAdsApi

from configs import limit as external_limit


def page_demography_analytics(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    params = {
        "metric": [
            "page_fans_gender_age",
            "page_fans_country"
        ]
    }

    fields = {
        InsightsResult.Field.id,
        InsightsResult.Field.title,
        InsightsResult.Field.period,
        InsightsResult.Field.values
    }

    return Page(fb_obj_id).get_insights(params=params, fields=fields)


obj_id = '101083561525503'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
access_token = 'EAAFZAzWeB7YsBAA30BVnVw2XgPT4FXla9z8XtTrthXMxnZAJCOdF9vbxWir3uxaCLuhjZAP4qOy0VDldZBTfOCK220uIT2v966LR9tJBK4cwq0LBMAA09jK9oLaj0TUDxOoeVvqrjT9bMZAGET4wkb0agjEIJ3WsDgZClj98wSkkKRZAdgZAqmMl8uc8Sqc0PLE9Eyomicq0lQZDZD'

test = page_demography_analytics(obj_id, app_id, app_secret, access_token)

print(test)

# print(json.dumps(test, indent=4))
