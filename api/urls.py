from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MikiList, MikiDetail # UserList, UserDetail, UserMikiList


urlpatterns = [
    url(r'^mikis/$', MikiList.as_view()),
    url(r'^mikis/(?P<pk>[0-9]+)$', MikiDetail.as_view()),
    #url(r'^users/$', UserList.as_view()),
    #url(r'^users/(?P<id>[0-9]+)$', UserDetail.as_view()),
    #url(r'^users/(?P<id>[0-9]+)/mikis/$', UserMikiList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)