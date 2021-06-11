from facebook_business.adobjects.iguser import IGUser
from facebook_business.api import FacebookAdsApi


def createIGPost(fb_obj_id, app_id, app_secret, access_token, caption=None, media_type=None, media=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if media:
        if media_type == 'image':
            params = {
                'caption': caption,
                'image_url': media[0]
            }
        elif media_type == 'video':
            params = {
                'caption': caption,
                'video_url': media[0]
            }
        else:
            return False

        try:
            id = IGUser(fb_obj_id).create_media(params=params)
            params = {
                "creation_id": id['id']
            }

            IGUser(fb_obj_id).create_media_publish(params=params)

            return True
        except:
            return False
    else:
        return False
