import json

from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.instagraminsightsresult import InstagramInsightsResult
from facebook_business.api import FacebookAdsApi

from facebook_business.adobjects.page import Page
from facebook_business.adobjects.insightsresult import InsightsResult

from datetime import datetime, timedelta


from facebook_business.adobjects.iguser import IGUser
from facebook_business.adobjects.igmedia import IGMedia
from facebook_business.api import FacebookAdsApi

from configs import limit as external_limit


def testing(obj_id, app_id, app_secret, access_token, page=True):
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
        "shortcode",
        "owner",
        "username",
        "timestamp",
        "permalink",
        "media_type",
        "media_url",
        "children{id,media_type,media_url,thumbnail_url}",
        "caption",
        "like_count",
        "is_comment_enabled",
        "comments_count"
    }

    params = {
        "limit": 100
    }

    if page:
        posts = IGUser(obj_id).get_media(fields=fields, params=params)
    else:
        posts = IGMedia(obj_id).api_get(fields=fields)

    output = []
    for idx, post in enumerate(posts):
        print(idx)
        fields = {
            InstagramInsightsResult.Field.id,
            InstagramInsightsResult.Field.title,
            InstagramInsightsResult.Field.period,
            InstagramInsightsResult.Field.values
        }

        try:
            params = {
                "metric": [
                    InstagramInsightsResult.Metric.impressions,
                    InstagramInsightsResult.Metric.reach,
                    InstagramInsightsResult.Metric.engagement,
                    InstagramInsightsResult.Metric.saved,
                    InstagramInsightsResult.Metric.video_views
                ],
                "period": [
                    InstagramInsightsResult.Period.lifetime
                ]
            }

            data = IGMedia(post["id"]).get_insights(params=params, fields=fields)
        except:
            params = {
                "metric": [
                    InstagramInsightsResult.Metric.impressions,
                    InstagramInsightsResult.Metric.reach,
                    InstagramInsightsResult.Metric.engagement,
                    InstagramInsightsResult.Metric.saved
                ],
                "period": [
                    InstagramInsightsResult.Period.lifetime
                ]
            }

            data = IGMedia(post["id"]).get_insights(params=params, fields=fields)

        try:
            video_views = data[4]["values"][0].get("value")
        except:
            video_views = 0

        output.append({
            "post_id": post["id"],
            "posted_on": post["timestamp"],
            "impressions": data[0]["values"][0].get("value") or 0,
            "reach": data[1]["values"][0].get("value") or 0,
            "engagement": data[2]["values"][0].get("value") or 0,
            "saved": data[3]["values"][0].get("value") or 0,
            "video_views": video_views
        })

    return output


obj_id = '17841431321059427'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
access_token = 'EAAFZAzWeB7YsBAFcbW3cthIru6Lxkt6wnT7w9OpoBZCWgaqDe2yFGVzX0qELfKlG2WY7JGA1wCESy6WX2cLOPlBVPt9yuCeU2yTHWeSyByiogyxe9XZA1yHvNIpWLs23i13xE2CcdYo0gmenWtZBgFK1vUfY7G1iFJhFwrsjxzG4MYuk4qdySOKx3ZB83VGNgp0hOaepqGQZDZD'

test = testing(obj_id, app_id, app_secret, access_token)

# print(test)

print(json.dumps(test, indent=4))
