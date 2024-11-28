from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('redirect/', views.redirect_me, name='redirect_me'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]