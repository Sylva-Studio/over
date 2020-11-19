from django.urls import path
from .views import home, post_detail, create_post, post_update, post_delete, featured

urlpatterns = [
  path('', home, name="home"),
  path('New/post/', featured, name="featured_post"),
  path('featured-post', create_post, name="create_post"),
  path('<pk>/post-detail/', post_detail, name="post_detail"),
  path('<pk>/post-update/', post_update, name="post_update"),
  path('<pk>/post-delete/', post_delete, name="post_delete"),
]