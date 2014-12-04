from __future__ import unicode_literals
from future.builtins import super

from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.messages import info, error, success

from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, DetailView

from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate

from .models import Link
from .utils import order_by_score


class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            qs = context["object_list"].filter(user=profile_user)
            context["object_list"] = qs
        context["profile_user"] = profile_user
        context["no_data"] = ("Sorry, there is no data here.")
        return context


class ScoreOrderingView(UserFilterView):
    """
    List view that optionally orders ``object_list`` by calculated
    score. Subclasses must defined a ``date_field`` attribute for the
    related model, that's used to determine time-scaled scoring.
    Ordering by score is the default behaviour, but can be
    overridden by passing ``False`` to the ``by_score`` arg in
    urlpatterns, in which case ``object_list`` is sorted by most
    recent, using the ``date_field`` attribute. Used for showing lists
    of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(ScoreOrderingView, self).get_context_data(**kwargs)
        qs = context["object_list"]
        context["by_score"] = self.kwargs.get("by_score", True)
        if context["by_score"]:
            qs = order_by_score(qs, self.score_fields, self.date_field)
        else:
            qs = qs.order_by("-" + self.date_field)
        context["object_list"] = paginate(qs, self.request.GET.get("page", 1),
            settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)
        context["title"] = self.get_title(context)
        return context


class LinkView(object):
    """
    List and detail view mixin for links - just defines the correct
    queryset.
    """
    def get_queryset(self):
        return Link.objects.published().select_related("user", "user__profile")


class LinkList(LinkView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("newest" main nav item).
    """

    date_field = "publish_date"
    score_fields = ("rating_sum", "comments_count")

    def get_title(self, context):
        if context["by_score"]:
            return ""  # Homepage
        if context["profile_user"]:
            return "%s" % context["profile_user"].profile
        else:
            return "Latest"



class LinkCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = modelform_factory(Link, fields=("title", "body"))
    model = Link

    def form_valid(self, form):
        if len(form.instance.title) > 50:
            error(self.request, "Sorry, miki's title must not exceed 50 characters limit.")
            return super(LinkCreate, self).form_invalid(form)
        if len(form.instance.body) > 200:
            error(self.request, "Sorry, miki's body must not exceed 200 characters limit.")
            return super(LinkCreate, self).form_invalid(form)
        hours = getattr(settings, "ALLOWED_DUPLICATE_LINK_HOURS", None)
        if form.instance.link:
            if hours:
                lookup = {
                    "link": form.instance.link,
                    "publish_date__gt": now() - timedelta(hours=hours),
                }
                try:
                    link = Link.objects.get(**lookup)
                except Link.DoesNotExist:
                    pass
                else:
                    error(self.request, "Miki with this link already exists")
                    return redirect(link)
        form.instance.user = self.request.user
        success(self.request, "Miki created")
        return super(LinkCreate, self).form_valid(form)




class LinkDetail(LinkView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """
    pass


class CommentList(ScoreOrderingView):
    """
    List view for comments, which can be for all users ("comments" and
    "best" main nav items) or a single user (comments from user's
    profile page). Comments can be order by score ("best" main nav item)
    or by most recently created ("comments" main nav item, profile
    comments).
    """

    date_field = "submit_date"
    score_fields = ("rating_sum",)

    def get_queryset(self):
        qs = ThreadedComment.objects.filter(is_removed=False, is_public=True)
        select = ("user", "user__profile",)
        prefetch = ("content_object",)
        return qs.select_related(*select).prefetch_related(*prefetch)

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        elif context["by_score"]:
            return "Best comments"
        else:
            return "Latest comments"

