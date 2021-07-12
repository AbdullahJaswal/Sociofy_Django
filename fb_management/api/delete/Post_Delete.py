from facebook_business.adobjects.post import Post
from facebook_business.api import FacebookAdsApi

from django.core.cache import cache


def deleteFBPost(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    try:
        Post(fb_obj_id).api_delete()

        cache.clear()
        return True
    except:
        return False
