from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.igcomment import IGComment
from facebook_business.api import FacebookAdsApi

from facebook_business.api import FacebookAdsApi


def createIGComment(fb_obj_id, app_id, app_secret, access_token, caption=None):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=True,
        crash_log=False
    )

    if caption:
        try:
            params = {
                'message': caption
            }

            IGMedia(fb_obj_id).create_comment(params=params)

            return True
        except:
            return False
    else:
        return False


obj_id = '18151403878199204'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
access_token = 'EAAFZAzWeB7YsBAPM6fE3icIZBl2aWyJmnJJPLJZAX4ddgxV1E5H3rhTPpHQuAzV0dfSZAQH5ceVqI2uD5MX005wGd2vW6WB64u2ZBEkZCX3SebMFpeRoPJpfxwSouy16dQ2xQhNh58bCqZAT8xmbflTvhhKkZAn8qz2BySTdv82Uqi63DiZASa6t8'
caption = "Recent"
image = "https://i.ibb.co/KNKYJn6/earth.jpg"

print(createIGComment(obj_id, app_id, app_secret, access_token, caption))
