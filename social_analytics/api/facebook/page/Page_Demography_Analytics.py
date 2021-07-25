from facebook_business.adobjects.page import Page
from facebook_business.adobjects.insightsresult import InsightsResult
from facebook_business.api import FacebookAdsApi


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
            "page_fans_country",
            "page_fans_city"
        ]
    }

    fields = {
        InsightsResult.Field.id,
        InsightsResult.Field.title,
        InsightsResult.Field.period,
        InsightsResult.Field.values
    }

    return Page(fb_obj_id).get_insights(params=params, fields=fields)
