import json

from .models import *
from sm_accounts.models import *
from fb_management.api.get.Page_Data import *
from fb_management.api.get.Post_Data import *
from fb_management.api.get.Comment_Data import *
from fb_management.api.post.Post_Create import *
from fb_management.api.post.Comment_Create import *
from fb_management.api.delete.Post_Delete import *
from fb_management.api.delete.Comment_Delete import *
from .jobs.post import *
from .sync.FBPostTags_Sync import *
from django.utils import timezone
from django.db.models import Q

from celery import group
from bulk_sync import bulk_sync  # noqa. <-- Used to suppress error highlight.

fb_app_number = 2  # Change to 1 after Facebook App Review!


# For ALL PAGES
def fetch_fb_pages_data(user):
    try:
        fb_accounts = FacebookAccounts.objects.filter(
            user=user.id)  # Get Facebook Page Accounts of User. Access Tokens!

        if fb_accounts.exists():
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            tasks = []
            for account in fb_accounts:
                tasks.append(
                    getFBPageData.s(account.facebook_id, fb_app.app_id, fb_app.app_secret, account.access_token)
                )

            task_group = group(*tasks)
            result_group = task_group.apply_async()
            data = result_group.join()

            pages = []
            if data:
                for i in range(len(data)):  # Used this loop because of sm_account. Needed 'i' value.
                    pages.append(FBPage(
                        user=user,
                        sm_account=fb_accounts[i],
                        page_id=data[i]['id'],
                        created_on=timezone.now(),
                        modified_on=timezone.now(),
                        name=data[i]['name'],
                        username=data[i]['username'],
                        fb_link=data[i]['link'],
                        verification_status=data[i]['verification_status'],
                        followers_count=data[i]['followers_count'],
                        likes=data[i]['fan_count'],
                        picture=data[i]['picture'],
                        cover=data[i]['cover'],
                        category=data[i]['category'],
                        about=data[i]['about'],
                        email=data[i]['email'],
                        phone=data[i]['phone'],
                        whatsapp_number=data[i]['whatsapp_number'],
                        website=data[i]['website'],
                        can_post=data[i]['can_post'],
                        connected_instagram_account=data[i]['connected_instagram_account'],
                    ))

            if pages:
                bulk_sync(
                    new_models=pages,
                    filters=[],  # Some field which is same in all records.
                    fields=[
                        'modified_on',
                        'name',
                        'username',
                        'verification_status',
                        'followers_count',
                        'likes',
                        'picture',
                        'cover',
                        'category',
                        'about',
                        'email',
                        'phone',
                        'whatsapp_number',
                        'website',
                        'can_post',
                        'connected_instagram_account',
                        'user'
                    ],
                    key_fields=('fb_link',),
                    exclude_fields=('id', 'sm_account', 'page_id', 'fb_link',),
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


# For SINGLE PAGE
def fetch_fb_page_data(local_page_id):
    try:
        page = FBPage.objects.select_related('sm_account').filter(id=local_page_id)

        if page.exists():
            page = FBPage.objects.select_related('sm_account').get(id=local_page_id)

            fb_app = FacebookApp.objects.get(id=fb_app_number)

            data = getFBPageData(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

            pages = []
            if data:
                pages.append(FBPage(
                    modified_on=timezone.now(),
                    name=data['name'],
                    username=data['username'],
                    fb_link=data['link'],
                    verification_status=data['verification_status'],
                    followers_count=data['followers_count'],
                    likes=data['fan_count'],
                    picture=data['picture'],
                    cover=data['cover'],
                    category=data['category'],
                    about=data['about'],
                    email=data['email'],
                    phone=data['phone'],
                    whatsapp_number=data['whatsapp_number'],
                    website=data['website'],
                    can_post=data['can_post'],
                    connected_instagram_account=data['connected_instagram_account'],
                ))

            if pages:
                bulk_sync(
                    new_models=pages,
                    filters=[],  # Some field which is same in all records.
                    fields=[
                        'modified_on',
                        'name',
                        'username',
                        'verification_status',
                        'followers_count',
                        'likes',
                        'picture',
                        'cover',
                        'category',
                        'about',
                        'email',
                        'phone',
                        'whatsapp_number',
                        'website',
                        'can_post',
                        'connected_instagram_account'
                    ],
                    key_fields=('fb_link',),
                    exclude_fields=('id', 'user', 'sm_account', 'page_id', 'fb_link',),
                    skip_creates=True,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


# For ALL POSTS
def fetch_fb_posts_data(local_page_id, user_id):
    try:
        page = FBPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)

        if page.exists():
            # Using 'get' makes it faster.
            page = FBPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)

            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Page ID is sent to get all posts data.
            data = getFBPostData(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token,
                                 page=True)

            posts = []
            tags = []
            if data:
                count = 0

                for obj in data:
                    count += 1

                    if 'message_tags' in obj:  # Only Hashtags of post.
                        for tag in obj['message_tags']:
                            if tag['name'][0] == '#':
                                tags.append({'id': tag['id'], 'tag': tag['name'], 'created_on': obj['created_time']})

                    media = None
                    link = None
                    if 'attachments' in obj:  # All media attachments of the post for Carousel.
                        if obj['attachments']['data'][0]['type'] != 'share':
                            media = post_media_attachments(obj)
                        else:
                            link = obj['attachments']['data'][0]['url']

                    reactions = None
                    if 'insights' in obj:  # All reactions of the post.
                        reactions = post_reactions(obj)

                    comment_count = 0
                    if 'comments' in obj:  # Count of all comments on the post.
                        comment_count = post_comments_count(obj)

                    posts.append(FBPost(
                        page=page,
                        post_id=obj.get('id') or None,
                        created_time=obj.get('created_time') or None,
                        updated_time=obj.get('updated_time') or None,
                        modified_on=timezone.now(),
                        application=True if 'application' in obj else False,
                        message=obj.get('message') or None,
                        link=link,
                        media=media,
                        timeline_visibility=obj.get('timeline_visibility') or None,
                        is_hidden=obj.get('is_hidden'),
                        is_published=obj.get('is_published'),
                        is_expired=obj.get('is_expired'),
                        permalink_url=obj.get('permalink_url') or None,
                        reactions=reactions,
                        comment_count=comment_count,
                        shares=obj['shares']['count'] if 'shares' in obj else 0,
                        privacy=obj['privacy']['value'] if 'privacy' in obj else None,
                        status_type=obj.get('status_type') or None
                    ))

                    if count == external_limit:
                        break

                if posts:
                    bulk_sync(
                        new_models=posts,
                        filters=Q(page=page.id),  # Field(s) which is same in all records.
                        fields=[
                            'updated_time',
                            'modified_on',
                            'application',
                            'message',
                            'link',
                            'media',
                            'timeline_visibility',
                            'is_hidden',
                            'is_published',
                            'is_expired',
                            'reactions',
                            'comment_count',
                            'shares',
                            'privacy',
                            'status_type'
                        ],
                        key_fields=('post_id',),
                        # Field(s) which is different in all records but always same for itself.
                        exclude_fields=('id', 'page', 'post_id', 'created_time', 'permalink_url',),
                        skip_deletes=False,
                        batch_size=50
                    )

                if tags:
                    tags_bulk_sync(tags, local_page_id)

            return True
        else:
            return False
    except:
        return False


# For SINGLE POST
def fetch_fb_post_data(local_page_id, user_id, local_post_id):
    try:
        post = FBPost.objects.filter(id=local_post_id)

        if post.exists():
            page = FBPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get that single post data only.
            obj = getFBPostData(post[0].post_id, fb_app.app_id, fb_app.app_secret, page[0].sm_account.access_token,
                                page=False)

            posts = []
            if obj:
                media = None
                link = None
                if 'attachments' in obj:  # All media attachments of the post for Carousel.
                    if obj['attachments']['data'][0]['type'] != 'share':
                        media = post_media_attachments(obj)
                    else:
                        link = obj['attachments']['data'][0]['type']['url']

                reactions = None
                if 'insights' in obj:  # All reactions of the post.
                    reactions = post_reactions(obj)

                comment_count = 0
                if 'comments' in obj:  # Count of all comments on the post.
                    comment_count = post_comments_count(obj)

                posts.append(FBPost(
                    post_id=obj.get('id') or None,
                    updated_time=obj.get('updated_time') or None,
                    modified_on=timezone.now(),
                    application=True if 'application' in obj else False,
                    message=obj.get('message') or None,
                    link=link,
                    media=media,
                    timeline_visibility=obj.get('timeline_visibility') or None,
                    is_hidden=obj.get('is_hidden'),
                    is_published=obj.get('is_published'),
                    is_expired=obj.get('is_expired'),
                    reactions=reactions,
                    comment_count=comment_count,
                    shares=obj['shares']['count'] if 'shares' in obj else 0,
                    privacy=obj['privacy']['value'] if 'privacy' in obj else None,
                    status_type=obj.get('status_type') or None
                ))

            if posts:
                bulk_sync(
                    new_models=posts,
                    filters=Q(page=page[0].id),  # Field(s) which is same in all records.
                    fields=[
                        'updated_time',
                        'modified_on',
                        'application',
                        'message',
                        'link',
                        'media',
                        'timeline_visibility',
                        'is_hidden',
                        'is_published',
                        'is_expired',
                        'reactions',
                        'comment_count',
                        'shares',
                        'privacy',
                        'status_type'
                    ],
                    key_fields=('post_id',),  # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'post_id', 'created_time', 'permalink_url',),
                    skip_creates=True,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def fetch_fb_post_comments_data(local_page_id, local_post_id, user_id):
    try:
        post = FBPost.objects.get(id=local_post_id)

        if post:
            page = FBPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get post comments data only.
            obj = getFBCommentData(post.post_id, fb_app.app_id, fb_app.app_secret, page[0].sm_account.access_token)

            comments = []
            if obj:
                for comment in obj:
                    replies_count = 0
                    replies = None

                    if 'comments' in comment:
                        replies = comment

                        replies_count += len(comment)

                    comments.append(FBPostComment(
                        post=post,
                        comment_id=comment.get('id') or None,
                        created_time=comment.get('created_time') or None,
                        modified_on=timezone.now(),
                        fb_user_id=comment['from']['id'] if 'from' in comment else None,
                        fb_user_name=comment['from']['name'] if 'from' in comment else None,
                        can_comment=comment.get('can_comment'),
                        attachment_type=comment['attachment']['type'] if 'attachment' in comment else None,
                        attachment=comment['attachment']['media']['image']['src'] if 'attachment' in comment else None,
                        message=comment.get('message') or None,
                        reactions_count=comment['reactions']['summary'].get('total_count') or None,
                        reactions=comment['reactions'].get('data') or None,
                        replies_count=replies_count,
                        replies=replies,
                    ))

            if comments:
                bulk_sync(
                    new_models=comments,
                    filters=Q(post=post.id),  # Field(s) which is same in all records.
                    fields=[
                        'modified_on',
                        'fb_user_name',
                        'attachment_type',
                        'attachment',
                        'message',
                        'reactions_count',
                        'reactions',
                        'replies_count',
                        'replies'
                    ],
                    key_fields=('comment_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'comment_id', 'created_time', 'fb_user_id', 'can_comment',),
                    skip_deletes=False,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def fetch_fb_post_comment_data(local_page_id, local_comment_id, user_id, local_post_id):
    try:
        comment = FBPostComment.objects.get(id=local_comment_id)

        if comment:
            page = FBPage.objects.select_related('sm_account').filter(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            # Post ID is sent to get post comments data only.
            obj = getFBCommentData(comment.comment_id, fb_app.app_id, fb_app.app_secret,
                                   page[0].sm_account.access_token, False)

            comments = []
            if obj:
                replies_count = 0
                replies = None

                if 'comments' in obj:
                    replies = obj['comments']['data']

                    replies_count += len(obj['comments']['data'])

                comments.append(FBPostComment(
                    comment_id=obj.get('id') or None,
                    created_time=obj.get('created_time') or None,
                    modified_on=timezone.now(),
                    fb_user_id=obj['from']['id'] if 'from' in obj else None,
                    fb_user_name=obj['from']['name'] if 'from' in obj else None,
                    can_comment=obj.get('can_comment'),
                    attachment_type=obj['attachment']['type'] if 'attachment' in obj else None,
                    attachment=obj['attachment']['media']['image']['src'] if 'attachment' in obj else None,
                    message=obj.get('message') or None,
                    reactions_count=obj['reactions']['summary'].get('total_count') or None,
                    reactions=obj['reactions'].get('data') or None,
                    replies_count=replies_count,
                    replies=replies,
                ))

            if comments:
                bulk_sync(
                    new_models=comments,
                    filters=Q(post=local_post_id),  # Field(s) which is same in all records.
                    fields=[
                        'modified_on',
                        'fb_user_name',
                        'attachment_type',
                        'attachment',
                        'message',
                        'reactions_count',
                        'reactions',
                        'replies_count',
                        'replies'
                    ],
                    key_fields=('comment_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'comment_id', 'created_time', 'fb_user_id', 'can_comment',),
                    skip_creates=True,
                    skip_deletes=True,
                    batch_size=50
                )

            return True
        else:
            return False
    except:
        return False


def create_fb_post(local_page_id, user_id, message=None, link=None, pictures=None, video=None):
    # try:
        page = FBPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)

        if page:
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return createFBPost(
                page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token,
                message=message, link=link, pictures=pictures, video=video
            )
    #     else:
    #         return False
    # except:
    #     return False


def delete_fb_post(local_page_id, user_id, local_post_id):
    try:
        post = FBPost.objects.get(id=local_post_id)

        if post:
            if post.application is True:
                page = FBPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)
                fb_app = FacebookApp.objects.get(id=fb_app_number)

                return deleteFBPost(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)
            else:
                return 0  # If the Post was not posted from the application.
        else:
            return False
    except:
        return False


def create_fb_post_comment(local_page_id, local_post_id, user_id, message=None, attachment_type=None, attachment=None):
    try:
        post = FBPost.objects.get(id=local_post_id)

        if post:
            page = FBPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return createFBComment(
                post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token,
                message, attachment_type, attachment
            )
        else:
            return False
    except:
        return False


def delete_fb_post_comment(local_page_id, user_id, local_comment_id):
    try:
        comment = FBPostComment.objects.get(id=local_comment_id)

        if comment:
            page = FBPage.objects.select_related('sm_account').get(id=local_page_id, user=user_id)
            fb_app = FacebookApp.objects.get(id=fb_app_number)

            return deleteFBPostComment(comment.comment_id, fb_app.app_id, fb_app.app_secret,
                                       page.sm_account.access_token)
        else:
            return False
    except:
        return False
