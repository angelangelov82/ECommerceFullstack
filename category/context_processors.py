from .models import Category


def menu_links(request): # fetch the categories from the database
    links = Category.objects.all() #store all categories in links var
    return dict(links=links)# it will bring all the categories list and will store them into the links var
