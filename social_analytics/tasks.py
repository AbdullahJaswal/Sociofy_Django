import json

import numpy as np

from .models import *
from sm_accounts.models import *
from social_analytics.api.instagram.page.Page_Analytics import *
from social_analytics.api.instagram.page.Page_Demography_Analytics import *
from social_analytics.api.instagram.page.daily.Impressions_Analytic import *
from social_analytics.api.instagram.page.daily.Reach_Analytic import *
from social_analytics.api.instagram.page.daily.Follower_Count_Analytic import *
from social_analytics.api.instagram.page.daily.Email_Contacts_Analytic import *
from social_analytics.api.instagram.page.daily.Phone_Call_Clicks_Analytic import *
from social_analytics.api.instagram.page.daily.Text_Message_Clicks_Analytic import *
from social_analytics.api.instagram.page.daily.Get_Direction_Clicks_Analytic import *
from social_analytics.api.instagram.page.daily.Website_Clicks_Analytic import *
from social_analytics.api.instagram.page.daily.Profile_Views_Analytic import *
from social_analytics.api.instagram.post.Post_Analytics import *
from django.utils import timezone
from django.db.models import Q

from celery import group
from bulk_sync import bulk_sync  # noqa. <-- Used to suppress error highlight.

fb_app_number = 2  # Change to 1 after Facebook App Review!


# For ALL PAGES
def fetch_ig_page_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = page_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            pageAnalytics = [
                IGPageAnalytic(
                    page=page,
                    pageID=page.page_id,
                    datetime=data[0]["values"][0].get("end_time") or None,
                    today=False,
                    impressions=data[0]["values"][0].get("value") or 0,
                    reach=data[1]["values"][0].get("value") or 0,
                    follower_count=None,
                    email_contacts=data[2]["values"][0].get("value") or 0,
                    phone_call_clicks=data[3]["values"][0].get("value") or 0,
                    text_message_clicks=data[4]["values"][0].get("value") or 0,
                    get_directions_clicks=data[5]["values"][0].get("value") or 0,
                    website_clicks=data[6]["values"][0].get("value") or 0,
                    profile_views=data[7]["values"][0].get("value") or 0,
                ),
                IGPageAnalytic(
                    page=page,
                    pageID=page.page_id,
                    datetime=data[0]["values"][1].get("end_time") or None,
                    today=True,
                    impressions=data[0]["values"][1].get("value") or 0,
                    reach=data[1]["values"][1].get("value") or 0,
                    follower_count=None,
                    email_contacts=data[2]["values"][1].get("value") or 0,
                    phone_call_clicks=data[3]["values"][1].get("value") or 0,
                    text_message_clicks=data[4]["values"][1].get("value") or 0,
                    get_directions_clicks=data[5]["values"][1].get("value") or 0,
                    website_clicks=data[6]["values"][1].get("value") or 0,
                    profile_views=data[7]["values"][1].get("value") or 0,
                )
            ]

            if pageAnalytics:
                bulk_sync(
                    new_models=pageAnalytics,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "today",
                        "impressions",
                        "reach",
                        "follower_count",
                        "email_contacts",
                        "phone_call_clicks",
                        "text_message_clicks",
                        "get_directions_clicks",
                        "website_clicks",
                        "profile_views"
                    ],
                    key_fields=('pageID', 'today',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_demography_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = page_demography_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            age_stuff = data[0]["values"][0]["value"]

            age_sorted = sorted(age_stuff.items())

            age_groups = {
                "13-17",
                "18-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65+",
            }

            age_data = {
                "M": {},
                "F": {},
                "U": {}
            }

            for item in age_sorted:
                for age_group in age_groups:
                    if age_group == item[0][2:]:
                        age_data[item[0][0]].update({age_group: item[1]})
                    elif age_group not in age_data[item[0][0]].keys():
                        age_data[item[0][0]].update({age_group: 0})

            age_stuff = age_data

            pageDemographyAnalytics = [IGPageDemographyAnalytic(
                page=page,
                pageID=page.page_id,
                datetime=data[0]["values"][0].get("end_time") or None,
                audience_gender_age=age_stuff or None,
                audience_locale=data[1]["values"][0].get("value") or None,
                audience_country=data[2]["values"][0].get("value") or None,
                audience_city=data[3]["values"][0].get("value") or None,
            )]

            if pageDemographyAnalytics:
                bulk_sync(
                    new_models=pageDemographyAnalytics,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "audience_gender_age",
                        "audience_locale",
                        "audience_country",
                        "audience_city"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_daily_impressions_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = impressions_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyImpressions(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        impressions=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "impressions"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_daily_reach_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = reach_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyReach(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        reach=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "reach"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_daily_follower_count_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = follower_count_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyFollowerCount(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        follower_count=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "follower_count"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_daily_email_contacts_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = email_contacts_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyEmailContacts(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        email_contacts=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "email_contacts"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_phone_call_clicks_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = phone_call_clicks_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyPhoneCallClicks(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        phone_call_clicks=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "phone_call_clicks"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_text_message_clicks_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = text_message_clicks_analytic(page.page_id, fb_app.app_id, fb_app.app_secret,
                                            page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyTextMessageClicks(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        text_message_clicks=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "text_message_clicks"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_directions_clicks_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = get_directions_clicks_analytic(page.page_id, fb_app.app_id, fb_app.app_secret,
                                              page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyDirectionsClicks(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        directions_clicks=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "directions_clicks"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_website_clicks_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = website_clicks_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyWebsiteClicks(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        website_clicks=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "website_clicks"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_page_daily_profile_views_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = profile_views_analytic(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for obj in data[0]["values"]:
                dailyData.append(
                    IGPageDailyProfileViews(
                        page=page,
                        pageID=page.page_id,
                        datetime=obj.get("end_time") or None,
                        profile_views=obj.get("value") or 0
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "profile_views"
                    ],
                    key_fields=('pageID', 'datetime'),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=True,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_post_analytics_data(page, post_id):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        post = IGPost.objects.get(id=post_id)

        # Page ID is sent to get all posts data.
        data = post_analytics(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            postAnalytics = [
                IGPostAnalytic(
                    post=post,
                    pageID=page.page_id,
                    postID=post.post_id,
                    updated_on=timezone.now(),
                    impressions=data["impressions"],
                    reach=data["reach"],
                    engagement=data["engagement"],
                    saved=data["saved"],
                    video_views=data["video_views"]
                )
            ]

            if postAnalytics:
                bulk_sync(
                    new_models=postAnalytics,
                    filters=Q(post=post.id),  # Field(s) which is same in all records.
                    fields=[
                        "updated_on",
                        "impressions",
                        "reach",
                        "engagement",
                        "saved",
                        "video_views"
                    ],
                    key_fields=('postID',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'pageID', 'postID',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

                return True
            else:
                return False
        else:
            return False
    except:
        return False


def fetch_ig_post_ratings(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        posts = IGPost.objects.filter(page=page)

        if posts:
            tasks = []
            for post in posts:
                tasks.append(
                    post_analytics.s(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)
                )

            task_group = group(*tasks)
            result_group = task_group.apply_async()
            tasksData = result_group.join()

            postImpressions = []
            for i in range(len(tasks)):
                postImpressions.append(tasksData[i]["impressions"])

            # List of percentiles (increment of 10%) from 0 to 100.
            percentile = []
            for i in range(0, 110, 10):
                percentile.append(round(np.percentile(postImpressions, i, axis=0)))

            postRatings = []

            # Assign ratings to the list of data.
            for i in range(len(postImpressions)):
                rate = 0
                for perc in percentile:
                    if postImpressions[i] <= perc:
                        print(postImpressions[i])
                        postRatings.append(
                            IGPostRating(
                                page=page,
                                post=posts[i],
                                pageID=page.page_id,
                                postID=posts[i].post_id,
                                datetime=timezone.now(),
                                rating=rate
                            )
                        )

                        break

                    rate += 0.5

            if postRatings:
                bulk_sync(
                    new_models=postRatings,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "rating"
                    ],
                    key_fields=('postID',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'post', 'pageID', 'postID',),
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
