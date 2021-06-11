def post_media_attachments(obj):
    media = []

    if 'source' in obj['attachments']['data'][0]['media']:
        media.append({
            'type': "video",
            'url': obj['attachments']['data'][0]['media']['source'] if 'attachments' in obj else None
        })
    elif 'image' in obj['attachments']['data'][0]['media']:
        key = list(obj['attachments']['data'][0]['media'].keys())

        media.append({
            'type': key[0],
            'url': obj['attachments']['data'][0]['media']['image']['src'] if 'attachments' in obj else None
        })

    if 'subattachments' in obj['attachments']['data'][0]:
        skip = True

        for sub in obj['attachments']['data'][0]['subattachments']['data']:
            if skip is False:
                media.append({
                    'type': sub['type'],
                    'url': sub['media']['image']['src'] if 'media' in sub else None
                })
            else:
                skip = False

    return media


def post_reactions(obj):
    reactions = {
        'total': 0,
        'like': 0,
        'love': 0,
        'wow': 0,
        'haha': 0,
        'sad': 0,
        'anger': 0
    }

    if 'like' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['like'] = obj['insights']['data'][0]['values'][0]['value']['like']
    if 'love' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['love'] = obj['insights']['data'][0]['values'][0]['value']['love']
    if 'wow' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['wow'] = obj['insights']['data'][0]['values'][0]['value']['wow']
    if 'haha' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['haha'] = obj['insights']['data'][0]['values'][0]['value']['haha']
    if 'sad' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['sad'] = obj['insights']['data'][0]['values'][0]['value']['sad']
    if 'anger' in obj['insights']['data'][0]['values'][0]['value']:
        reactions['anger'] = obj['insights']['data'][0]['values'][0]['value']['anger']

    reactions['total'] = reactions['like'] + reactions['love'] + reactions['wow'] + reactions['haha'] + \
                         reactions['sad'] + reactions['anger']

    return reactions


def post_comments_count(obj):
    comment_count = 0

    for comment in obj['comments']['data']:
        comment_count += int(comment['comment_count'])
        comment_count += 1

    return comment_count
