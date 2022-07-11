from .models import Category, Post, Reply
# Hice esta función boluda cuando no estaba enterado
# del funcionamiento de admin/
def create_category(name):
    category = Category(name=name)
    category.save()
    return category

def clear_posts():
    Post.objects.all().delete()
    Reply.objects.all().delete()
    return