import json

from .models import *
from sm_accounts.models import *
from social_analytics.api.instagram.page.Page_Analytics import *
from social_analytics.api.instagram.page.Page_Demography_Analytics import *
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
