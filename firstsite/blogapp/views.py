from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.syndication.views import Feed



from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Author, Article, Category, Tag
from .serializers import AuthorSerializer, ArticleSerializer, CategorySerializer, TagSerializer


class ArticleListView(ListView):
    template_name = "blogapp/article_list.html"
    queryset = (
        Article.objects
        .select_related("author")
        .select_related("category")
        .prefetch_related("tags")
    )   

class ArticleDetailView(DetailView):
    model = Article



class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles")
    
    def items(self):
        return (
            Article.objects
            .filter(pub_date__isnull=False)
            .select_related("author")
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-pub_date")[:5]
        )
        
    def item_title(self, item: Article):
        return item.title
    
    def item_description(self, item: Article):
        str_arr = [item.category.name]#.extend(item.tags)
        return "".join(str_arr)
    
    def item_link(self, item: Article):
        return reverse("blogapp:article-details", kwargs={"pk": item.pk})






class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = (
            "name",
            "bio", 
        )
    filterset_fields = (
            "name",
            "bio",
        )
    ordering_fields = (
            "pk",
            "name",
            "bio", 
        )

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.prefetch_related("author").all()
    serializer_class = ArticleSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = (            
            "title",
            "content",
            "pub_date",
            "author",
            "category",
            "tags", 
        )
    filterset_fields = (
            "title",
            "content",
            "pub_date",
            "author",
            "category",
            "tags",
        )
    ordering_fields = (
            "pk",
            "title",
            "content",
            "pub_date",
            "author",
            "category",
            "tags",
        )

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



    