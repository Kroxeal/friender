from django.urls import path, re_path
from .views import *

# маршутизация
urlpatterns = [
    path('main/', main_page, name="main"),
    path('friends/', all_friends, name="friends"),
    path('establishments/', PlaceListView.as_view(), name="establishments"),
    path('static_url/', static_url, name="static_url"),
    path('user_rating/', user_rating, name="user_rating"),
    re_path(r"^user_rating/(?P<id>[\d-]+)$", user_form_rating, name="user_form_rating"),
    path('create_user/', create_user, name="create_user"),
    path('make_arrangements/', make_arrangements, name="make_arrangements"),
    path('create_place/', EstablishmentsCreateView.as_view()),

    # path('class_view/',MyTemplateView.as_view())
]