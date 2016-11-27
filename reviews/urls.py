from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /whisky/
    url(r'^whisky$', views.whisky_list, name='whisky_list'),
    # ex: /whisky/5/
    url(r'^whisky/(?P<whisky_id>[0-9]+)/$', views.whisky_detail, name='whisky_detail'),
    url(r'^whisky/(?P<whisky_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
]