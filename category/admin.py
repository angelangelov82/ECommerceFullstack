from django.contrib import admin
from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}#autofill the slug in admin/category when add
    list_display = ('category_name', 'slug')
admin.site.register(Category, CategoryAdmin) # register the admin
