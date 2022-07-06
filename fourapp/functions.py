from .models import Category
# Hice esta función boluda cuando no estaba enterado
# del funcionamiento de admin/
def create_category(name):
    category = Category(name=name)
    category.save()
    return category