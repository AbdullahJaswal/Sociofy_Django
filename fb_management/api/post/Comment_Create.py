from facebook_business.adobjects.post import Post
from facebook_business.api import FacebookAdsApi


def createFBComment(fb_obj_id, app_id, app_secret, access_token, message=None, attachment_type=None, attachment=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if attachment_type == 'photo':
        params = {
            'message': message,
            'attachment_url': attachment
        }

        try:
            Post(fb_obj_id).create_comment(params=params)
            return True
        except:
            return False
    elif message or attachment_type:
        params = {
            'message': message,
            'attachment_share_url': attachment
        }

        try:
            Post(fb_obj_id).create_comment(params=params)
            return True
        except:
            return False
