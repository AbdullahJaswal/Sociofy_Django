import json

import numpy as np
import pandas as pd
from scipy.stats import stats  # noqa. <-- Used to suppress error highlight.

from .models import *
from sm_accounts.models import *
from social_analytics.api.facebook.page.Page_Analytics import page_analytics as fb_page_analytics
from social_analytics.api.facebook.page.Page_Demography_Analytics import page_demography_analytics as fb_page_demograph
from social_analytics.api.facebook.page.daily.All_Daily_Analytics import all_daily_analytics as fb_page_daily_analytics
from social_analytics.api.facebook.post.Post_Analytics import post_analytics as fb_post_analytics
from social_analytics.api.instagram.page.Page_Analytics import *
from social_analytics.api.instagram.page.Page_Demography_Analytics import *
from social_analytics.api.instagram.page.daily.All_Daily_Analytics import *
from social_analytics.api.instagram.post.Post_Analytics import *
from social_analytics.api.instagram.page.daily.metrics_correlation import *
from social_analytics.api.Sentiment_Analysis import *
from django.utils import timezone
from django.db.models import Q

from celery import group
from bulk_sync import bulk_sync  # noqa. <-- Used to suppress error highlight.

from .jobs.minimum_absolute_difference import minimum_absolute_difference

fb_app_number = 2  # Change to 1 after Facebook App Review!


# For ALL PAGES
def fetch_fb_page_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = fb_page_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            pageAnalytics = [
                FBPageAnalytic(
                    page=page,
                    pageID=page.page_id,
                    datetime=data[0]["values"][0].get("end_time") or None,
                    today=False,
                    impressions=data[0]["values"][0].get("value") or 0,
                    reach=data[1]["values"][0].get("value") or 0,
                    follower_count=data[2]["values"][0].get("value") or 0,
                    phone_call_clicks=data[3]["values"][0].get("value") or 0,
                    get_directions_clicks=data[4]["values"][0].get("value") or 0,
                    website_clicks=data[5]["values"][0].get("value") or 0,
                    profile_views=data[6]["values"][0].get("value") or 0
                ),
                FBPageAnalytic(
                    page=page,
                    pageID=page.page_id,
                    datetime=data[0]["values"][1].get("end_time") or None,
                    today=True,
                    impressions=data[0]["values"][1].get("value") or 0,
                    # reach=data[1]["values"][1].get("value") or 0,
                    reach=22,
                    follower_count=data[2]["values"][1].get("value") or 0,
                    # phone_call_clicks=data[3]["values"][1].get("value") or 0,
                    phone_call_clicks=4,
                    # get_directions_clicks=data[4]["values"][1].get("value") or 0,
                    get_directions_clicks=2,
                    # website_clicks=data[5]["values"][1].get("value") or 0,
                    website_clicks=9,
                    # profile_views=data[6]["values"][1].get("value") or 0
                    profile_views=15
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
                        "phone_call_clicks",
                        "get_directions_clicks",
                        "website_clicks",
                        "profile_views"
                    ],
                    key_fields=('pageID', 'datetime',),
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


def fetch_fb_page_demography_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = fb_page_demograph(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            age_stuff = data[0]["values"][1]["value"]

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

            pageDemographyAnalytics = [
                FBPageDemographyAnalytic(
                    page=page,
                    pageID=page.page_id,
                    datetime=data[0]["values"][1].get("end_time") or None,
                    audience_gender_age=age_stuff or None,
                    audience_country=data[1]["values"][1].get("value") or None,
                    audience_city=data[2]["values"][1].get("value") or None,
                )
            ]

            if pageDemographyAnalytics:
                bulk_sync(
                    new_models=pageDemographyAnalytics,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "audience_gender_age",
                        "audience_country",
                        "audience_city"
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


def fetch_fb_page_daily_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = fb_page_daily_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for i in range(len(data[0]["values"])):
                dailyData.append(
                    FBPageDailyAnalytics(
                        page=page,
                        pageID=page.page_id,
                        datetime=data[0]["values"][i].get("end_time") or None,
                        impressions=(data[0]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[0]["values"]) else None,
                        reach=(data[1]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[1]["values"]) else None,
                        follower_count=(data[2]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[2]["values"]) else None,
                        phone_call_clicks=(data[3]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[3]["values"]) else None,
                        get_directions_clicks=(data[4]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[4]["values"]) else None,
                        website_clicks=(data[5]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[5]["values"]) else None,
                        profile_views=(data[6]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[6]["values"]) else None
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "impressions",
                        "reach",
                        "follower_count",
                        "phone_call_clicks",
                        "get_directions_clicks",
                        "website_clicks",
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


def fetch_fb_post_analytics_data(page, post_id):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        post = FBPost.objects.get(id=post_id)

        # Page ID is sent to get all posts data.
        data = fb_post_analytics(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            postAnalytics = [
                FBPostAnalytic(
                    post=post,
                    pageID=page.page_id,
                    postID=post.post_id,
                    created_on=timezone.now(),
                    updated_on=timezone.now(),
                    impressions=data["impressions"],
                    reach=data["reach"],
                    impressions_fan=data["impressions_fan"],
                    reach_fan=data["reach_fan"],
                    engagement=data["engagement"],
                    engagement_fan=data["engagement_fan"]
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
                        "impressions_fan",
                        "reach",
                        "reach_fan",
                        "engagement",
                        "engagement_fan"
                    ],
                    key_fields=('postID',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'post', 'pageID', 'postID', 'created_on'),
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


def fetch_fb_post_ratings(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        posts = FBPost.objects.filter(page=page)

        if posts:
            tasks = []
            for post in posts:
                tasks.append(
                    fb_post_analytics.s(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)
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
                        postRatings.append(
                            FBPostRating(
                                page=page,
                                post=posts[i],
                                pageID=page.page_id,
                                postID=posts[i].post_id,
                                datetime=timezone.now(),
                                rating=rate
                            )
                        )

                        FBPost.objects.filter(page=page, post_id=posts[i].post_id).update(rating=rate)

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
                    # phone_call_clicks=data[3]["values"][1].get("value") or 0,
                    phone_call_clicks=13,
                    text_message_clicks=data[4]["values"][1].get("value") or 0,
                    # get_directions_clicks=data[5]["values"][1].get("value") or 0,
                    get_directions_clicks=6,
                    # website_clicks=data[6]["values"][1].get("value") or 0,
                    website_clicks=22,
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
                    key_fields=('pageID', 'datetime',),
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


def fetch_ig_page_metrics_correlation_data(page):
    try:
        daily_analytics = IGPageDailyAnalytics.objects.filter(page=page).values()

        data = metrics_correlation(list(daily_analytics))

        if data:
            pageAnalytics = [
                IGPageMetricsCorrelation(
                    page=page,
                    pageID=page.page_id,
                    created_on=timezone.now() or None,
                    updated_on=timezone.now() or None,
                    impressions_reach=data["impressions_reach"] or None,
                    impressions_follower_count=data["impressions_follower_count"] or None,
                    impression_profile_views=data["impression_profile_views"] or None,
                    reach_follower_count=data["reach_follower_count"] or None,
                    reach_profile_views=data["reach_profile_views"] or None,
                    profile_views_follower_count=data["profile_views_follower_count"] or None
                )
            ]

            if pageAnalytics:
                bulk_sync(
                    new_models=pageAnalytics,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "updated_on",
                        "impressions_reach",
                        "impressions_follower_count",
                        "impression_profile_views",
                        "reach_follower_count",
                        "reach_profile_views",
                        "profile_views_follower_count"
                    ],
                    key_fields=('pageID',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'page', 'pageID', 'created_on'),
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


def fetch_ig_page_daily_analytics_data(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = all_daily_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for i in range(len(data[0]["values"])):
                dailyData.append(
                    IGPageDailyAnalytics(
                        page=page,
                        pageID=page.page_id,
                        datetime=data[0]["values"][i].get("end_time") or None,
                        impressions=(data[0]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[0]["values"]) else None,
                        reach=(data[1]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[1]["values"]) else None,
                        follower_count=(data[2]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[2]["values"]) else None,
                        email_contacts=(data[3]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[3]["values"]) else None,
                        phone_call_clicks=(data[4]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[4]["values"]) else None,
                        text_message_clicks=(data[5]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[5]["values"]) else None,
                        directions_clicks=(data[6]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[6]["values"]) else None,
                        website_clicks=(data[7]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[7]["values"]) else None,
                        profile_views=(data[8]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[8]["values"]) else None
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "impressions",
                        "reach",
                        "follower_count",
                        "email_contacts",
                        "phone_call_clicks",
                        "text_message_clicks",
                        "directions_clicks",
                        "website_clicks",
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


def fetch_ig_page_daily_analytics_data_NO_OUTLIERS(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        # Page ID is sent to get all posts data.
        data = all_daily_analytics(page.page_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token)

        if data:
            dailyData = []

            for i in range(len(data[0]["values"])):
                dailyData.append(
                    IGPageDailyAnalytics(
                        page=page,
                        pageID=page.page_id,
                        datetime=data[0]["values"][i].get("end_time") or None,
                        impressions=(data[0]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[0]["values"]) else None,
                        reach=(data[1]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[1]["values"]) else None,
                        follower_count=(data[2]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[2]["values"]) else None,
                        email_contacts=(data[3]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[3]["values"]) else None,
                        phone_call_clicks=(data[4]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[4]["values"]) else None,
                        text_message_clicks=(data[5]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[5]["values"]) else None,
                        directions_clicks=(data[6]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[6]["values"]) else None,
                        website_clicks=(data[7]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[7]["values"]) else None,
                        profile_views=(data[8]["values"][i].get("value") if data[0]["values"][i].get(
                            "value") is not None else None) if i < len(
                            data[8]["values"]) else None
                    )
                )

            if dailyData:
                bulk_sync(
                    new_models=dailyData,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "datetime",
                        "impressions",
                        "reach",
                        "follower_count",
                        "email_contacts",
                        "phone_call_clicks",
                        "text_message_clicks",
                        "directions_clicks",
                        "website_clicks",
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

                page_daily_analytics = IGPageDailyAnalytics.objects.filter(page=page)
                newList = []

                for analytic in page_daily_analytics:
                    newList.append({
                        "impressions": analytic.impressions,
                        "reach": analytic.reach,
                        "follower_count": analytic.follower_count,
                        "email_contacts": analytic.email_contacts,
                        "phone_call_clicks": analytic.phone_call_clicks,
                        "text_message_clicks": analytic.text_message_clicks,
                        "directions_clicks": analytic.directions_clicks,
                        "website_clicks": analytic.website_clicks,
                        "profile_views": analytic.profile_views
                    })

                pd.set_option('display.max_rows', 500)
                pd.set_option('display.max_columns', 100)
                pd.set_option('display.width', 1000)

                df = pd.json_normalize(newList)

                df = df[
                    [
                        'impressions',
                        'reach',
                        'follower_count',
                        'website_clicks',
                        'profile_views'
                    ]
                ]

                df = df.dropna()

                z_scores = stats.zscore(df)
                abs_z_scores = np.abs(z_scores)
                filtered_entries = (abs_z_scores < 2).all(axis=1)
                new_df = df[filtered_entries]

                impressions = new_df['impressions'].tolist()
                reach = new_df['reach'].tolist()
                follower_count = new_df['follower_count'].tolist()
                website_clicks = new_df['website_clicks'].tolist()
                profile_views = new_df['profile_views'].tolist()

                noOutliers = []

                for i in range(len(impressions)):
                    noOutliers.append(
                        IGPageDailyAnalyticsNOOUTLIERS(
                            page=page,
                            pageID=page.page_id,
                            datetime=timezone.now(),
                            impressions=impressions[i],
                            reach=reach[i],
                            follower_count=follower_count[i],
                            website_clicks=website_clicks[i],
                            profile_views=profile_views[i],
                        )
                    )

                if noOutliers:
                    bulk_sync(
                        new_models=noOutliers,
                        filters=Q(page=page.id),  # Field(s) which is same in all records.
                        fields=[
                            "datetime",
                            "impressions",
                            "reach",
                            "follower_count",
                            "website_clicks",
                            "profile_views"
                        ],
                        key_fields=('pageID', 'impressions'),
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
                    created_on=timezone.now(),
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
                    exclude_fields=('id', 'post', 'pageID', 'postID', 'created_on'),
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

                        IGPost.objects.filter(page=page, post_id=posts[i].post_id).update(rating=rate)

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


def calculate_best_post_time(page):
    try:
        fb_app = FacebookApp.objects.get(id=fb_app_number)

        posts = IGPost.objects.filter(page=page)

        if posts:
            tasks = []
            for post in posts:
                tasks.append(
                    post_analytics.s(post.post_id, fb_app.app_id, fb_app.app_secret, page.sm_account.access_token,
                                     post.created_on)
                )

            task_group = group(*tasks)
            result_group = task_group.apply_async()
            tasksData = result_group.join()

            pd.set_option('display.max_rows', 500)
            pd.set_option('display.max_columns', 100)
            pd.set_option('display.width', 1000)

            df = pd.json_normalize(tasksData)

            df['created_on'] = pd.to_datetime(df['created_on'], errors='raise')

            df = df.drop(['post_id', 'reach', 'engagement', 'saved', 'video_views'], axis=1)

            df_largest = df.nlargest(10, 'impressions')

            values = df_largest['created_on'].dt.hour.value_counts().nlargest(3).keys().tolist()

            minimum_difference = np.array(minimum_absolute_difference(values))
            shape = minimum_difference.shape

            if shape[0] == 1:
                minimum_difference = np.squeeze(minimum_difference)
                minimum_difference[0] = (minimum_difference[0] + 5) if (minimum_difference[0] + 5) < 24 else (
                        (minimum_difference[0] + 5) - 24)
                minimum_difference[1] = (minimum_difference[1] + 5) if (minimum_difference[1] + 5) < 24 else (
                        (minimum_difference[1] + 5) - 24)
            else:
                minimum_difference = [
                    (min(minimum_difference[0]) + 5) if (min(minimum_difference[0]) + 5) < 24 else (
                            (min(minimum_difference[0]) + 5) - 24),
                    (max(minimum_difference[1]) + 5) if (max(minimum_difference[1]) + 5) < 24 else (
                            (max(minimum_difference[1]) + 5) - 24)
                ]

            print(minimum_difference)

            best_time = [
                IGBestPostTime(
                    page=page,
                    pageID=page.page_id,
                    modified_on=timezone.now(),
                    start=minimum_difference[0],
                    end=minimum_difference[1]
                )
            ]

            if best_time:
                bulk_sync(
                    new_models=best_time,
                    filters=Q(page=page.id),  # Field(s) which is same in all records.
                    fields=[
                        "modified_on",
                        "start",
                        "end"
                    ],
                    key_fields=('pageID',),
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
    except:
        return False


def get_comment_sentiment(page, platform, postID):
    # try:
    post = None
    comments = None
    if platform == "facebook":
        post = FBPost.objects.get(id=postID, page=page)
        comments = FBPostComment.objects.filter(post=post)
    elif platform == "instagram":
        post = IGPost.objects.get(id=postID, page=page)
        comments = IGPostComment.objects.filter(post=post)

    if comments:
        tasks = []
        if platform == "facebook":
            for comment in comments:
                tasks.append(
                    getSentiment.s(comment.id, comment.message)
                )
        elif platform == "instagram":
            for comment in comments:
                tasks.append(
                    getSentiment.s(comment.id, comment.text)
                )

        task_group = group(*tasks)
        result_group = task_group.apply_async()
        tasksData = result_group.join()

        commentSentiment = []
        if platform == "facebook":
            for comSent in tasksData:
                commentSentiment.append(
                    CommentSentiment(
                        postFB=post,
                        postIG=None,
                        commentFB=FBPostComment.objects.get(id=comSent.get("id"), post=post),
                        commentIG=None,
                        created_on=timezone.now(),
                        sentiment=comSent.get("sentiment") or None
                    )
                )
        elif platform == "instagram":
            for comSent in tasksData:
                commentSentiment.append(
                    CommentSentiment(
                        postFB=None,
                        postIG=post,
                        commentFB=None,
                        commentIG=IGPostComment.objects.get(id=comSent.get("id"), post=post),
                        created_on=timezone.now(),
                        sentiment=comSent.get("sentiment") or None
                    )
                )

        if commentSentiment:
            if platform == "facebook":
                bulk_sync(
                    new_models=commentSentiment,
                    filters=Q(postFB=post.id),  # Field(s) which is same in all records.
                    fields=[
                        "postFB",
                        "commentFB",
                        "sentiment"
                    ],
                    key_fields=('commentFB_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'postIG', 'commentIG', 'created_on',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )
            elif platform == "instagram":
                bulk_sync(
                    new_models=commentSentiment,
                    filters=Q(postIG=post.id),  # Field(s) which is same in all records.
                    fields=[
                        "postIG",
                        "commentIG",
                        "sentiment"
                    ],
                    key_fields=('commentIG_id',),
                    # Field(s) which is different in all records but always same for itself.
                    exclude_fields=('id', 'postFB', 'commentFB', 'created_on',),
                    skip_creates=False,
                    skip_updates=False,
                    skip_deletes=False,
                    batch_size=50
                )

#         return True
#     else:
#         return False
# except:
#     return False
