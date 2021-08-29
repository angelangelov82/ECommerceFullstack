from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True) # URL for the Category
    description = models.TextField(max_length=255,  blank=True)
    cat_image = models.ImageField(upload_to ='photos/category', blank=True)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories' #fixes the typo in adminsite Categories to Category

    def get_url(self):
            return reverse('products_by_category', args=[self.slug])#it will the url of the particular category

    def __str__(self):
        return self.category_name
