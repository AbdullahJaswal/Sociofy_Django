from facebook_business.adobjects.iguser import IGUser
from facebook_business.api import FacebookAdsApi
import requests
import base64

from django.core.cache import cache


def createIGPost(fb_obj_id, app_id, app_secret, access_token, caption=None, media_type=None, media=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if media and media is not None:
        if media[0] is not None:
            if media_type == 'image':
                file_path = "/usr/src/sociofy/backend/media/" + media[0]

                with open(file_path, "rb") as image:
                    url = "https://api.imgbb.com/1/upload"
                    api_key = "799fb189a04183d6671800a48da0098c"
                    expiration = 300

                    payload = {
                        "key": api_key,
                        "expiration": expiration,
                        "image": base64.b64encode(image.read()),
                    }

                    response = requests.post(url, payload).json()

                    params = {
                        'caption': caption,
                        'image_url': response["data"]["url"]
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

                cache.clear()
                return True
            except:
                return False
        else:
            return False
    else:
        return False
