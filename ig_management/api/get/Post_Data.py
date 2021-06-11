from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.api import FacebookAdsApi

from configs import limit as external_limit


def getIGPostData(ig_obj_id, app_id, app_secret, access_token, page=True):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    fields = {
        "id",
        "ig_id",
        "shortcode",
        "owner",
        "username",
        "timestamp",
        "permalink",
        "media_type",
        "media_url",
        "children{id,media_type,media_url,thumbnail_url}",
        "caption",
        "like_count",
        "is_comment_enabled",
        "comments_count"
    }

    params = {
        "limit": external_limit
    }

    if page:
        data = IGUser(ig_obj_id).get_media(fields=fields, params=params)
    else:
        data = IGMedia(ig_obj_id).api_get(fields=fields)

    return data
