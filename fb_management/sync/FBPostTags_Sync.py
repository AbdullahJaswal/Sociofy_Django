from django.db.models import Q
from bulk_sync import bulk_sync  # noqa. <-- Used to suppress error highlight.
from background_task import background  # noqa. <-- Used to suppress error highlight.
from fb_management.models import FBPage, FBPostTag
from django.utils import timezone


# @shared_task
@background(schedule=0)  # Start at 0 seconds of execution.
def tags_bulk_sync(tags, local_page_id):
    page = FBPage.objects.filter(id=local_page_id)

    tagObjs = []
    for tag in tags:
        tagObjs.append(FBPostTag(
            page=page[0],
            tag_id=tag['id'],
            tag=tag['tag'],
            created_on=tag['created_on'],
            modified_on=timezone.now()
        ))

    bulk_sync(
        new_models=tagObjs,
        filters=Q(page=page[0].id),  # Field(s) which is same in all records.
        fields=[
            'tag',
            'modified_on'
        ],
        key_fields=('tag_id',),  # Field(s) which is different in all records but always same for itself.
        exclude_fields=('id', 'page', 'tag_id', 'created_on',),
        skip_deletes=True,
        batch_size=200
    )
