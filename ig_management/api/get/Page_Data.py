from facebook_business.adobjects.iguser import IGUser
from facebook_business.api import FacebookAdsApi

from celery import shared_task


@shared_task
def getIGPageData(ig_obj_id, app_id, app_secret, access_token):
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
        "name",
        "username",
        "profile_picture_url",
        "followers_count",
        "follows_count",
        "website",
        "biography",
        "media_count"
    }

    data = IGUser(ig_obj_id).api_get(fields=fields)

    followers_count = 0
    follows_count = 0
    media_count = 0

    if 'followers_count' in data:
        followers_count = 0 if data['followers_count'] is None else data['followers_count']

    if 'follows_count' in data:
        follows_count = 0 if data['follows_count'] is None else data['follows_count']

    if 'media_count' in data:
        media_count = 0 if data['media_count'] is None else data['media_count']

    page = {
        'id': data.get('id') or None,
        'ig_id': data.get('ig_id') or None,
        'name': data.get('name') or None,
        'username': data.get('username') or None,
        'profile_picture_url': data.get(
            'profile_picture_url') or "https://image.flaticon.com/icons/png/512/64/64572.png",
        'followers_count': followers_count,
        'follows_count': follows_count,
        'website': data.get('website') or None,
        'biography': data.get('biography') or None,
        'media_count': media_count
    }

    return page
