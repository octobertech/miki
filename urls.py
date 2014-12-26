from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns("",
	("^api/", include("api.urls")),
    ("^admin/", include(admin.site.urls)),
    ("^", include("main.urls")),
    ("^", include("mezzanine.urls")),
    ('^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

# Adds ``STATIC_URL`` to the context.
handler500 = "mezzanine.core.views.server_error"
