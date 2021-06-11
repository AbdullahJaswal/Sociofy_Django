from facebook_business.adobjects.post import Post
from facebook_business.adobjects.comment import Comment
from facebook_business.api import FacebookAdsApi

from configs import limit as external_limit


def getFBCommentData(fb_obj_id, app_id, app_secret, access_token, all_comments=True):
    FacebookAdsApi.init(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        debug=False,
        crash_log=False
    )

    if all_comments:
        fields = [
            'id',
            'created_time',
            'from',
            'can_comment',
            'attachment',
            'message',
            'reactions.summary(total_count)',
            'comment_count',
            'comments{id,created_time,from,can_comment,attachment,message,reactions.summary(total_count)}'
        ]

        params = {
            'limit': external_limit,
        }

        data = Post(fb_obj_id).get_comments(fields=fields, params=params)
    else:
        fields = [
            'id',
            'created_time',
            'from',
            'can_comment',
            'attachment',
            'message',
            'reactions.summary(total_count)',
            'comment_count',
            'comments{id,created_time,from,can_comment,attachment,message,reactions.summary(total_count)}'
        ]

        data = Comment(fb_obj_id).api_get(fields=fields)

    return data
