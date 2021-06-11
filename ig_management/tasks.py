import json

from .models import *
from sm_accounts.models import *
from ig_management.api.get.Page_Data import *
from ig_management.api.get.Post_Data import *
from ig_management.api.post.Create_Post import *
from ig_management.api.get.Comment_Data import *
from ig_management.api.get.Reply_Data import *
from ig_management.api.post.Create_Comment import *
from ig_management.api.delete.Delete_Comment import *
from django.utils import timezone
from django.db.models import Q

from celery import group
from bulk_sync import bulk_sync  # noqa. <-- Used to suppress error highlight.

fb_app_number = 2  # Change to 1 after Facebook App Review!


# For ALL PAGES
def fetch_ig_pages_data(user):
    try:
        # Get Instagram Page Accounts of User. Access Tokens!
        ig_accounts = InstagramAccounts.objects.filter(user=user.id)

        if ig_accounts.exists():
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            tasks = []
            for account in ig_accounts:
                tasks.append(
                    getIGPageData.s(account.instagram_id, fb_app.app_id, fb_app.app_secret, account.access_token))

            task_group = group(*tasks)
            result_group = task_group.apply_async()
            data = result_group.join()

            pages = []
            if data:
                for i in range(len(data)):  # Used this loop because of sm_account. Needed 'i' value.
                    pages.append(IGPage(
                        user=user,
                        sm_account=ig_accounts[i],
                        page_id=data[i]['id'],
                        page_ig_id=data[i]['ig_id'],
                        modified_on=timezone.now(),
                        name=data[i]['name'],
                        username=data[i]['username'],
                        picture=data[i]['profile_picture_url'],
                        followers_count=data[i]['followers_count'],
                        follows_count=data[i]['follows_count'],
                        website=data[i]['website'],
                        biography=data[i]['biography'],
                        media_count=data[i]['media_count'],
                    ))

            if pages:
                bulk_sync(
                    new_models=pages,
                    filters=[],  # Some field which is same in all records.
                    fields=[
                        'modified_on',
                        'name',
                        'username',
                        'picture',
                        'followers_count',
                        'follows_count',
                        'website',
                        'biography',
                        'media_count'
                    ],
                    key_fields=('page_id',),  # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'user', 'sm_account', 'page_id', 'page_ig_id',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


# For SINGLE PAGE
def fetch_ig_page_data(local_page_id):
    try:
        page = IGPage.objects.select_related('sm_account').filter(id=local_page_id)

        if page.exists():
            page = IGPage.objects.select_related('sm_account').get(id=local_page_id)

            fb_app = FacebookApp.objects.get(id=fb_app_number)

            data = getIGPageData(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

            pages = []
            if data:
                pages.append(IGPage(
                    page_id=data['id'],
                    page_ig_id=data['ig_id'],
                    modified_on=timezone.now(),
                    name=data['name'],
                    username=data['username'],
                    picture=data['profile_picture_url'],
                    followers_count=data['followers_count'],
                    follows_count=data['follows_count'],
                    website=data['website'],
                    biography=data['biography'],
                    media_count=data['media_count'],
                ))

            if pages:
                bulk_sync(
                    new_models=pages,
                    filters=[],  # Some field which is same in all records.
                    fields=[
                        'modified_on',
                        'name',
                        'username',
                        'picture',
                        'followers_count',
                        'follows_count',
                        'website',
                        'biography',
                        'media_count'
                    ],
                    key_fields=('page_id',),  # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'user', 'sm_account', 'page_id', 'page_ig_id',),
                    skip_creates=True,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


# For ALL POSTS
def fetch_ig_posts_data(local_page_id, user_id):
    try:
        page = IGPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)

        if page.exists():
            # Using 'get' makes it faster.
            page = IGPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)

            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Page ID is sent to get all posts data.
            data = getIGPostData(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

            posts = []
            if data:
                count = 0

                for obj in data:
                    count += 1

                    if 'children' in obj:  # All media attachments of the post for Carousel.
                        media = obj['children']['data']
                    elif 'media_url' in obj:
                        media = [{
                            "media_url": obj['media_url'],
                            "media_type": obj['media_type']
                        }]
                    else:
                        media = None

                    posts.append(IGPost(
                        page=page,
                        post_id=obj.get('id') or None,
                        post_ig_id=obj.get('ig_id') or None,
                        shortcode=obj.get('shortcode') or None,
                        owner=obj['owner'].get('id') or None,
                        username=obj.get('username') or None,
                        created_on=obj.get('timestamp') or None,
                        modified_on=timezone.now(),
                        ig_link=obj.get('permalink') or None,
                        media_type=obj.get('media_type') or None,
                        media=media,
                        caption=obj.get('caption') or None,
                        like_count=obj.get('like_count') or 0,
                        can_comment=obj.get('is_comment_enabled'),
                        comment_count=obj.get('comments_count') or 0,
                    ))

                    if count == external_limit:
                        break

                if posts:
                    bulk_sync(
                        new_models=posts,
                        filters=Q(page=page.id),  # Field(s) which is same in all records.
                        fields=[
                            'username',
                            'modified_on',
                            'media_type',
                            'media',
                            'caption',
                            'like_count',
                            'can_comment',
                            'comment_count'
                        ],
                        key_fields=('post_id',),
                        # Field(s) which is different in all records but always same for itself.
                        exclude_fields=('id', 'page', 'post_id', 'post_ig_id', 'shortcode', 'created_on', 'ig_link',),
                        skip_creates=False,
                        skip_updates=False,
                        skip_deletes=False,
                        batch_size=50
                    )

            return True
        else:
            return False
    except:
        return False


# For SINGLE POST
def fetch_ig_post_data(local_page_id, user_id, local_post_id):
    try:
        post = IGPost.objects.filter(id=local_post_id)

        if post.exists():
            page = IGPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get that single post data only.
            obj = getIGPostData(post[0].post_id, fb_app.app_id, fb_app.app_secret, page[0].sm_account.access_token,
                                page=False)

            posts = []
            if obj:
                if 'children' in obj:  # All media attachments of the post for Carousel.
                    media = obj['children']['data']
                elif 'media_url' in obj:
                    media = [{
                        "media_url": obj['media_url'],
                        "media_type": obj['media_type']
                    }]
                else:
                    media = None

                posts.append(IGPost(
                    post_id=obj.get('id') or None,
                    post_ig_id=obj.get('ig_id') or None,
                    shortcode=obj.get('shortcode') or None,
                    owner=obj['owner'].get('id') or None,
                    username=obj.get('username') or None,
                    created_on=obj.get('timestamp') or None,
                    modified_on=timezone.now(),
                    ig_link=obj.get('permalink') or None,
                    media_type=obj.get('media_type') or None,
                    media=media,
                    caption=obj.get('caption') or None,
                    like_count=obj.get('like_count') or None,
                    can_comment=obj.get('is_comment_enabled'),
                    comment_count=obj.get('comments_count') or None,
                ))

            if posts:
                bulk_sync(
                    new_models=posts,
                    filters=Q(page=page[0].id),  # Field(s) which is same in all records.
                    fields=[
                        'username',
                        'modified_on',
                        'media_type',
                        'media',
                        'caption',
                        'like_count',
                        'can_comment',
                        'comment_count'
                    ],
                    key_fields=('post_id',),  # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'post_id', 'post_ig_id', 'shortcode', 'created_on', 'ig_link',),
                    skip_creates=True,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def create_ig_post(local_page_id, user_id, caption=None, media_type=None, media=None):
    try:
        page = IGPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)

        if page:
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return createIGPost(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token, caption,
                                media_type, media)
        else:
            return False
    except:
        return False


def fetch_ig_post_comments_data(local_page_id, local_post_id, user_id):
    try:
        post = IGPost.objects.get(id=local_post_id)

        if post:
            page = IGPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get post comments data only.
            obj = getIGCommentData(post.post_id, fb_app.app_id, fb_app.app_secret, page[0].sm_account.access_token)

            comments = []
            if obj:
                for comment in obj:
                    comment_user_id = None
                    if 'user' in comment:
                        comment_user_id = comment['user']['id']

                    media_user_id = None
                    if 'media' in comment:
                        media_user_id = comment['media']['id']

                    # replies = getIGCommentReplyData(comment.get('id'), fb_app.app_id, fb_app.app_secret,
                    #                                 page[0].sm_account.access_token)
                    #
                    # try:
                    #     replies_count = len(replies)
                    # except:
                    #     replies_count = 0

                    comments.append(IGPostComment(
                        post=post,
                        comment_id=comment.get('id') or None,
                        ig_user_id=comment_user_id,
                        ig_user_name=comment.get('username') or None,
                        created_on=comment.get('timestamp') or None,
                        modified_on=timezone.now(),
                        is_hidden=comment.get('hidden'),
                        text=comment.get('text') or None,
                        like_count=comment.get('like_count') or 0,
                        replies_count=None,
                        replies=None,
                        comment_post_id=media_user_id,
                    ))

            if comments:
                bulk_sync(
                    new_models=comments,
                    filters=Q(post=post.id),  # Field(s) which is same in all records.
                    fields=[
                        'ig_user_name',
                        'modified_on',
                        'is_hidden',
                        'text',
                        'like_count',
                        'replies_count',
                        'replies'
                    ],
                    key_fields=('comment_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'comment_id', 'ig_user_id', 'created_on', 'comment_post_id',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def fetch_ig_post_comment_data(local_page_id, local_comment_id, user_id, local_post_id):
    try:
        comment = IGPostComment.objects.get(id=local_comment_id)

        if comment:
            page = IGPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get post comments data only.
            obj = getIGCommentData(comment.comment_id, fb_app.app_id, fb_app.app_secret,
                                   page[0].sm_account.access_token, False)

            comments = []
            if obj:
                comment_user_id = None
                if 'user' in obj:
                    comment_user_id = obj['user']['id']

                media_user_id = None
                if 'media' in obj:
                    media_user_id = obj['media']['id']

                replies = getIGCommentReplyData(obj.get('id'), fb_app.app_id, fb_app.app_secret,
                                                page[0].sm_account.access_token)

                try:
                    replies_count = len(replies)
                except:
                    replies_count = 0

                comments.append(IGPostComment(
                    comment_id=obj.get('id') or None,
                    ig_user_id=comment_user_id,
                    ig_user_name=obj.get('username') or None,
                    created_on=obj.get('timestamp') or None,
                    modified_on=timezone.now(),
                    is_hidden=obj.get('hidden'),
                    text=obj.get('text') or None,
                    like_count=obj.get('like_count') or 0,
                    replies_count=replies_count,
                    replies=replies,
                    comment_post_id=media_user_id,
                ))

            if comments:
                bulk_sync(
                    new_models=comments,
                    filters=Q(post=local_post_id),  # Field(s) which is same in all records.
                    fields=[
                        'ig_user_name',
                        'modified_on',
                        'is_hidden',
                        'text',
                        'like_count',
                        'replies_count',
                        'replies'
                    ],
                    key_fields=('comment_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'comment_id', 'ig_user_id', 'created_on', 'comment_post_id',),
                    skip_creates=True,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def create_ig_post_comment(local_page_id, local_post_id, user_id, message=None):
    try:
        post = IGPost.objects.get(id=local_post_id)

        if post:
            page = IGPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return createIGComment(
                post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token,
                message
            )
        else:
            return False
    except:
        return False


def delete_ig_post_comment(local_page_id, user_id, local_comment_id):
    try:
        comment = IGPostComment.objects.get(id=local_comment_id)

        if comment:
            page = IGPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return deleteIGPostComment(comment.comment_id, fb_app.app_id, fb_app.app_secret,
                                       page.sm_account.access_token)
        else:
            return False
    except:
        return False
