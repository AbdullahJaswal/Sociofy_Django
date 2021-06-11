import time

import requests
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.post import Post
from facebook_business.api import FacebookAdsApi

import json

# table = [
#     {'A', 'B', 'E', 'G', 'J', 'L'},
#     {'B', 'C', 'D', 'F', 'I'},
#     {'A', 'B', 'E'},
#     {'A', 'B', 'C', 'F', 'G', 'I', 'K', 'L'},
#     {'B', 'C', 'D', 'E'},
#     {'A', 'C', 'D', 'F', 'J', 'L'},
#     {'A', 'B', 'F', 'G'},
#     {'A', 'B', 'E', 'H', 'J', 'K', 'L'},
#     {'C', 'D', 'F', 'H', 'K'},
#     {'A', 'B', 'E', 'F', 'I', 'L'}
# ]
#
# products = [
#     {'name': 'B', 'count': 8},
#     {'name': 'A', 'count': 7},
#     {'name': 'F', 'count': 6},
#     {'name': 'E', 'count': 5},
#     {'name': 'L', 'count': 5},
#     {'name': 'C', 'count': 5},
#     {'name': 'D', 'count': 4},
#     {'name': 'G', 'count': 3},
#     {'name': 'J', 'count': 3},
#     {'name': 'I', 'count': 3},
#     {'name': 'K', 'count': 3},
#     {'name': 'H', 'count': 2}
# ]
#
# support = []
# for x in range(len(products)):
#     index = []
#
#     for i in range(len(table)):
#         for item in table[i]:
#             if products[x]['name'] == item:
#                 index.append(i)
#
#     support.append({
#         'product': [
#             products[x]['name']
#         ],
#         'support': str(products[x]['count'] * 10) + '%'
#     })
#
#     for y in range(len(products)):
#         if y > x:
#             count = 0
#             index2 = []
#
#             for i in range(len(index)):
#                 if products[y]['name'] in table[index[i]]:
#                     index2.append(i)
#                     count += 1
#
#             for z in range(len(products)):
#                 if z > y:
#                     count2 = 0
#                     index3 = []
#
#                     for i in range(len(index2)):
#                         if products[z]['name'] in table[index[index2[i]]]:
#                             index3.append(i)
#                             count2 += 1
#
#                     for a in range(len(products)):
#                         if a > z:
#                             count3 = 0
#
#                             for i in range(len(index3)):
#                                 if products[a]['name'] in table[index[index2[index3[i]]]]:
#                                     count3 += 1
#
#                             if count3 >= 3:
#                                 support.append({
#                                     'product': [
#                                         products[x]['name'],
#                                         products[y]['name'],
#                                         products[z]['name'],
#                                         products[a]['name']
#                                     ],
#                                     'support': str(count3 * 10) + '%',
#                                     'confidence': [
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[z]['name'] + ' - '
#                                                            + products[a]['name'] + ' -> ' + products[x]['name']
#                                         },
#                                         {
#                                             'transaction': products[x]['name'] + ' - ' + products[z]['name'] + ' - '
#                                                            + products[a]['name'] + ' -> ' + products[y]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[x]['name'] + ' - '
#                                                            + products[a]['name'] + ' -> ' + products[z]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[x]['name'] + ' - '
#                                                            + products[z]['name'] + ' -> ' + products[a]['name']
#                                         },
#                                         {
#                                             'transaction': products[x]['name'] + ' -> ' + products[y]['name'] + ' - '
#                                                            + products[z]['name'] + ' - ' + products[a]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' -> ' + products[x]['name'] + ' - '
#                                                            + products[z]['name'] + ' - ' + products[a]['name']
#                                         },
#                                         {
#                                             'transaction': products[z]['name'] + ' -> ' + products[y]['name'] + ' - '
#                                                            + products[x]['name'] + ' - ' + products[a]['name']
#                                         },
#                                         {
#                                             'transaction': products[a]['name'] + ' -> ' + products[y]['name'] + ' - '
#                                                            + products[x]['name'] + ' - ' + products[z]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[z]['name'] + ' -> '
#                                                            + products[a]['name'] + ' - ' + products[x]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[a]['name'] + ' -> '
#                                                            + products[z]['name'] + ' - ' + products[x]['name']
#                                         },
#                                         {
#                                             'transaction': products[y]['name'] + ' - ' + products[x]['name'] + ' -> '
#                                                            + products[z]['name'] + ' - ' + products[a]['name']
#                                         },
#                                         {
#                                             'transaction': products[a]['name'] + ' - ' + products[x]['name'] + ' -> '
#                                                            + products[y]['name'] + ' - ' + products[z]['name']
#                                         },
#                                         {
#                                             'transaction': products[a]['name'] + ' - ' + products[y]['name'] + ' -> '
#                                                            + products[z]['name'] + ' - ' + products[x]['name']
#                                         },
#                                         {
#                                             'transaction': products[a]['name'] + ' - ' + products[z]['name'] + ' -> '
#                                                            + products[x]['name'] + ' - ' + products[y]['name']
#                                         },
#                                     ]
#                                 })
#
#                     if count2 >= 3:
#                         support.append({
#                             'product': [
#                                 products[x]['name'],
#                                 products[y]['name'],
#                                 products[z]['name']
#                             ],
#                             'support': str(count2 * 10) + '%',
#                             'confidence': [
#                                 {
#                                     'transaction': products[y]['name'] + ' - ' + products[z]['name'] + ' -> ' +
#                                                    products[x]['name'],
#                                 },
#                                 {
#                                     'transaction': products[x]['name'] + ' - ' + products[z]['name'] + ' -> ' +
#                                                    products[y]['name']
#                                 },
#                                 {
#                                     'transaction': products[x]['name'] + ' - ' + products[y]['name'] + ' -> ' +
#                                                    products[z]['name']
#                                 },
#                                 {
#                                     'transaction': products[x]['name'] + ' -> ' + products[y]['name'] + ' - ' +
#                                                    products[z]['name']
#                                 },
#                                 {
#                                     'transaction': products[y]['name'] + ' -> ' + products[x]['name'] + ' - ' +
#                                                    products[z]['name']
#                                 },
#                                 {
#                                     'transaction': products[z]['name'] + ' -> ' + products[x]['name'] + ' - ' +
#                                                    products[y]['name']
#                                 }
#                             ]
#                         })
#
#             if count >= 3:
#                 support.append({
#                     'product': [
#                         products[x]['name'],
#                         products[y]['name']
#                     ],
#                     'support': str(count * 10) + '%',
#                     'confidence': [
#                         {
#                             'transaction': products[x]['name'] + ' -> ' + products[y]['name'],
#                             'confidence': str(round((count / products[x]['count']) * 100, 2)) + '%'
#                         },
#                         {
#                             'transaction': products[y]['name'] + ' -> ' + products[x]['name'],
#                             'confidence': str(round((count / products[y]['count']) * 100, 2)) + '%'
#                         }
#                     ]
#                 })
#
# print(json.dumps(support, indent=4))

# for i in range(len(products)):
#     for row in table:
#         count = 0
#         item = [None, None]
#
#         for item1 in row:
#             if products[i] == item1:
#                 for item2 in row:
#                     if i != len(products) - 1:
#                         if products[i + 1] == item2:
#                             item[0] = item1
#                             item[1] = item2
#                             count += 1
#
#         if item[0] is not None and item[1] is not None:
#             print(item[0], ' - ', item[1], ' : ', count)

# def createFBPost(fb_obj_id, app_id, app_secret, access_token, message=None, link=None, pictures=None, video=None):
#     FacebookAdsApi.init(
#         app_id=app_id,
#         app_secret=app_secret,
#         access_token=access_token,
#         debug=True,
#         crash_log=False
#     )
#
#     if pictures:
#         params = {
#             'message': message
#         }
#         count = 0
#
#         for picture in pictures:
#             # Image uploaded to imgbb to get the image url link for Instagram
#             file = open(picture, 'rb')
#             param = {
#                 'key': '184949793f9ce02459619020945528f6',
#                 'expiration': 60
#             }
#             image = {'image': file}
#             print('Uploading image...')
#             imgbbResponse = requests.post("https://api.imgbb.com/1/upload", data=param, files=image).json()
#             picture_url = imgbbResponse["data"]["url"]
#
#             uploadParams = {
#                 'url': picture_url,
#                 'published': False
#             }
#
#             try:
#                 id = Page(fb_obj_id).create_photo(params=uploadParams)
#
#                 param = 'attached_media[' + str(count) + ']'
#                 params[param] = {'media_fbid': id['id']}
#
#                 count += 1
#             except:
#                 return False
#
#         time.sleep(3)
#
#         try:
#             print(Page(fb_obj_id).create_feed(params=params))
#             return True
#         except:
#             return False
#     elif message or link:
#         params = {
#             'message': message,
#             'link': link
#         }
#
#         try:
#             Page(fb_obj_id).create_feed(params=params)
#             return True
#         except:
#             return False


from facebook_business.adobjects.post import Post
from facebook_business.adobjects.comment import Comment
from facebook_business.api import FacebookAdsApi
import requests
import base64

import datetime

from configs import limit as external_limit


def testing(fb_obj_id, app_id, app_secret, access_token, all_comments=True):
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


page_id = '112531917317825'
obj_id = '101083561525503_317286869905170'
app_id = '380213716446603'
app_secret = 'f3bc4ff1f73d798c443cfed13badbd06'
apparel_access_token = "EAAFZAzWeB7YsBADDFIRChP20jZAilIEPxkmHwjmRIRAgZAOln9zZAMIOVj5ObPH6cZCo80FVCJfjese7cQpWZAXS3zHcowqSekfS3STZBivDpDIQXI7EAVSg6mIghR5roMAToHBBDx0WsuVO5fmMRI7GhIEnFPxHoFjr8eVqZCayYoZA4aDyT6w2LzdTQVjARcLkZD"
dummy_access_token = 'EAAFZAzWeB7YsBAPM6fE3icIZBl2aWyJmnJJPLJZAX4ddgxV1E5H3rhTPpHQuAzV0dfSZAQH5ceVqI2uD5MX005wGd2vW6WB64u2ZBEkZCX3SebMFpeRoPJpfxwSouy16dQ2xQhNh58bCqZAT8xmbflTvhhKkZAn8qz2BySTdv82Uqi63DiZASa6t8'
message = '...'
link = 'https://i.ibb.co/Z6Yj0wB/universe.jpg'
schedule = round(datetime.datetime(2021, 5, 24, 12, 56, 0).timestamp())
mediaPath = [
    "/Users/abdullahjaswal/Pictures/uploads/can-of-coke.jpg"
]

data = testing(obj_id, app_id, app_secret, apparel_access_token)

print(data)
