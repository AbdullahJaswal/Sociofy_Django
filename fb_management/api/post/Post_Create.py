from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookAdsApi
import requests
import base64

from django.core.cache import cache


def createFBPost(fb_obj_id, app_id, app_secret, access_token, message=None, link=None, pictures=None, video=None,
                 schedule=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if pictures and pictures is not None:
        params = {
            'message': message
        }
        count = 0

        for picture in pictures:
            if picture is not None:
                file_path = "/usr/src/sociofy/backend/media/" + picture

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

                    uploadParams = {
                        'url': response["data"]["url"],
                        'published': False
                    }

                    try:
                        id = Page(fb_obj_id).create_photo(params=uploadParams)

                        param = 'attached_media[' + str(count) + ']'
                        params[param] = {'media_fbid': id['id']}

                        count += 1
                    except:
                        return False
            else:
                return False
        try:
            Page(fb_obj_id).create_feed(params=params)

            cache.clear()
            return True
        except:
            return False
    elif message:
        if schedule is None:
            params = {
                'message': message,
            }

            try:
                Page(fb_obj_id).create_feed(params=params)

                cache.clear()
                return True
            except:
                return False
        else:
            params = {
                'message': message,
                'published': False,
                'scheduled_publish_time': schedule,
            }

            try:
                Page(fb_obj_id).create_feed(params=params)

                cache.clear()
                return True
            except:
                return False
