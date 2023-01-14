from django.urls import path

from .views import *

urlpatterns = [
  path('', home, name="home"),
  path('login/', login_view, name="login"),
  path('register/', register_view, name="register"),
  path('logout/', logout_trigger, name="logout"),
  path('add-followee/<str:id>', add_followee, name="add_followee"),
  path('follower-profile/<str:id>', follower_profile, name="follower_profile"),
  path('remove-followee/<str:id>', remove_followee, name="remove_followee"),
  path('settings/', settings, name="settings"),
  path('likes/<str:id>', likes, name="likes"),
  path('unlike/<str:id>', unlike, name="unlike"),
  path('add_post/', add_post, name="add_post"),
  path('add_comment/<str:id>', add_comment, name="add_comment"),
  path('delete_post/<str:id>', delete_post, name="delete_post"),
]