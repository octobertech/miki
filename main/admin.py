from __future__ import unicode_literals

from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from main.models import Link


class LinkAdmin(DisplayableAdmin):

    list_display = ("id", "title", "body", "keywords", "description",  "status", "publish_date",
                    "user", "comments_count", "rating_sum")
    list_display_links = ("id",)
    list_editable = ("title", "body", "description", "status")
    list_filter = ("status", "user__username", "keywords",)
    ordering = ("-publish_date",)

    fieldsets = (
        (None, {
            "fields": ("title", "body", "keywords", "link", "status", "publish_date", "user"),
        }),
    )


admin.site.register(Link, LinkAdmin)
