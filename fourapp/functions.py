from .models import Category

def create_category(name):
    category = Category(name=name)
    category.save()
    return category