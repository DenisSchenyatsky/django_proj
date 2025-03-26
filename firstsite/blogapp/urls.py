from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleListView,
    ArticleDetailView,
    
    LatestArticlesFeed,
    
    AuthorViewSet,
    ArticleViewSet,
    CategoryViewSet,
    TagViewSet,
)

app_name = "blogapp"

routers = DefaultRouter()
routers.register("authors", AuthorViewSet)
routers.register("articles", ArticleViewSet)
routers.register("categories", CategoryViewSet)
routers.register("tags", TagViewSet)

urlpatterns = [
      path("api/", include(routers.urls)),
      path("articles/", ArticleListView.as_view(), name="articles"),
      path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-details"),
      path("articles/latest/feed/", LatestArticlesFeed(), name="article-feed"),
]



    
