from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookAdsApi

from configs import limit as external_limit


def getFBPostData(fb_obj_id, app_id, app_secret, access_token, page):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    fields = {
        'id',
        'created_time',
        'updated_time',
        'full_picture',
        'application',
        'message',
        'timeline_visibility',
        'is_hidden',
        'is_published',
        'is_expired',
        'message_tags',
        'permalink_url',
        'shares',
        'privacy',
        'status_type',
        'attachments',
        'insights.metric(post_reactions_by_type_total){values}',
        'comments{id,comment_count}'
    }

    params = {
        'limit': external_limit,
    }

    if page is True:
        data = Page(fb_obj_id).get_posts(fields=fields, params=params)
    else:
        data = Page(fb_obj_id).api_get(fields=fields)

    return data
