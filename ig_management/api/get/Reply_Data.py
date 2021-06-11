from facebook_business.adobjects.igcomment import IGComment
from facebook_business.api import FacebookAdsApi


def getIGCommentReplyData(fb_obj_id, app_id, app_secret, access_token):
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

    data = IGComment(fb_obj_id).get_replies(fields=fields)

    json = None
    if data:
        json = []

        for comment in data:
            comment_user_id = None
            if 'user' in comment:
                comment_user_id = int(comment['user']['id'])

            media_user_id = None
            if 'media' in comment:
                media_user_id = int(comment['media']['id'])

            json.append({
                "id": int(comment.get('id') or None),
                "user": comment_user_id,
                "username": comment.get('username') or None,
                "timestamp": comment.get('timestamp') or None,
                "hidden": comment.get('hidden'),
                "text": comment.get('text') or None,
                "like_count": int(comment.get('like_count')) or 0,
                "media": media_user_id
            })

    return json
