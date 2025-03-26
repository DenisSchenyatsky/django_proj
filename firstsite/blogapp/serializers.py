from rest_framework import serializers

from .models import Author, Article, Category, Tag

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            "pk",
            "name",
            "bio",
        )


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "content",
            "pub_date",
            "author",
            "category",
            "tags",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
        )
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
        )