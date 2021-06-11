from facebook_business.adobjects.page import Page
from facebook_business.api import FacebookAdsApi

from celery import shared_task


@shared_task
def getFBPageData(fb_obj_id, app_id, app_secret, access_token):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    fields = [
        'id',
        'name',
        'username',
        'link',
        'verification_status',
        'followers_count',
        'fan_count',
        'picture.height(320).width(320)',
        'cover',
        'category',
        'about',
        'emails',
        'phone',
        'whatsapp_number',
        'website',
        'can_post',
        'connected_instagram_account',
    ]

    data = Page(fb_obj_id).api_get(fields=fields)

    page = {
        'id': data.get('id') or None,
        'name': data.get('name') or None,
        'username': data.get('username') or None,
        'link': data.get('link') or None,
        'verification_status': data.get('verification_status') or None,
        'followers_count': data.get('followers_count') or None,
        'fan_count': data.get('fan_count') or None,
        'picture': data['picture']["data"].get('url') or "https://image.flaticon.com/icons/png/512/64/64572.png",
        'cover': data['cover'].get('source') or None,
        'category': data.get('category') or None,
        'about': data.get('about') or None,
        'email': data['emails'][0] if 'emails' in data else None,
        # Facebook returns emails as a list. This code only selects the first one.
        'phone': data.get('phone') or None,
        'whatsapp_number': '+' + data['whatsapp_number'] if 'whatsapp_number' in data else None,
        # Add '+' to WhatsApp number since it's not done by default.
        'website': data.get('website') or None,
        'can_post': data.get('can_post'),
        'connected_instagram_account': data['connected_instagram_account'].get('id') or None
    }

    return page
