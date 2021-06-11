from facebook_business.adobjects.comment import Comment
from facebook_business.api import FacebookAdsApi


def deleteFBPostComment(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    try:
        Comment(fb_obj_id).api_delete()
        return True
    except:
        return False
