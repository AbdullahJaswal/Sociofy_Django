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

    params = {
        "metric": [
            "audience_gender_age",
            "audience_locale",
            "audience_country",
            "audience_city"
        ],
        "period": [
            InstagramInsightsResult.Period.lifetime
        ]
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
access_token = 'EAAFZAzWeB7YsBADDFIRChP20jZAilIEPxkmHwjmRIRAgZAOln9zZAMIOVj5ObPH6cZCo80FVCJfjese7cQpWZAXS3zHcowqSekfS3STZBivDpDIQXI7EAVSg6mIghR5roMAToHBBDx0WsuVO5fmMRI7GhIEnFPxHoFjr8eVqZCayYoZA4aDyT6w2LzdTQVjARcLkZD'

print(testing(obj_id, app_id, app_secret, access_token))
