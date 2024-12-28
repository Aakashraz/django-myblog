from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    # Post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # both above patterns points to the same view, but they have different names.
    # The first pattern will call the post_list view without any optional parameters,
    #  whereas the second pattern will call the view with the tag_slug parameter.
    # path('', views.PostListView.as_view(), name='post_list'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('redirect/', views.redirect_me, name='redirect_me'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

]
