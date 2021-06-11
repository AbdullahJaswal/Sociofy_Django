from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.api import FacebookAdsApi


def createIGComment(fb_obj_id, app_id, app_secret, access_token, message=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if message:
        try:
            params = {
                'message': message
            }

            IGMedia(fb_obj_id).create_comment(params=params)

            return True
        except:
            return False
    else:
        return False
