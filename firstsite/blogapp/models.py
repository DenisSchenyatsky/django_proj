from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100, null=False, db_index=True)
    bio = models.TextField(null=True, blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=40, db_index=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    
class Article(models.Model):
    title = models.CharField(max_length=200, null=False, db_index=True)
    content = models.TextField() # default null=False, blank=False 
    pub_date = models.DateTimeField(auto_now_add=True)
    # null=True чтоб можно было задним числом добавлять
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    tags = models.ManyToManyField(Tag, related_name="articles")
    
    def get_absolute_url(self):
        return reverse("blogapp:article-details", kwargs={"pk": self.pk})
    
    
