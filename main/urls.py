from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import index, LinkList, LinkCreate, LinkDetail, LinkDelete, CommentList, follow, unfollow, users


urlpatterns = patterns("",
    url("^$", 
        index, 
        name="timeline"),
    url("^discover/$",
        LinkList.as_view(),
        name="home"),
    url("^discover/latest/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_latest"),
    url("^discover/users/$",
        users,
        name="users"),
    url("^discover/comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_latest"),
    url("^discover/comments/best/$",
        CommentList.as_view(),
        name="comment_list_best"),
    url("^m/create/$",
        login_required(LinkCreate.as_view()),
        name="link_create"),
    url("^m/(?P<slug>.*)/$",
        LinkDetail.as_view(),
        name="link_detail"),
    url("^m/(?P<pk>\w+)/delete/*$",
        LinkDelete.as_view(),
        name="link_delete"),
    url("^users/(?P<username>.*)/$",
        users, name="link_list_user"),
    url(r'^follow/$', follow, name='follow'),
    url(r'^unfollow/$', unfollow, name='unfollow'),
    url("^users/(?P<username>.*)/comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_user"),
)
