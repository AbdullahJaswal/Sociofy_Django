from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.igcomment import IGComment
from facebook_business.api import FacebookAdsApi


def getIGCommentData(fb_obj_id, app_id, app_secret, access_token, all_comments=True):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    fields = [
        'id',
        'user',
        'username',
        'timestamp',
        'text',
        'like_count',
        'hidden',
        'media'
    ]

    params = {
        "limit": 200
    }

    if all_comments:
        data = IGMedia(fb_obj_id).get_comments(fields=fields, params=params)
    else:
        data = IGComment(fb_obj_id).api_get(fields=fields)

    return data
