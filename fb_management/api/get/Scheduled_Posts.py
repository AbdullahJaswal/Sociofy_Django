from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookAdsApi


def getFBScheduledPostsData(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    try:
        data = Page(fb_obj_id).get_scheduled_posts()
    except:
        data = None

    return data
