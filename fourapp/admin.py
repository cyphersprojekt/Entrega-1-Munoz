from django.contrib import admin
from .models import Category, Post, Reply

# Register your models here.


#Agregamos estas cosinhas para agregar categorías y posts desde el panel de administrador en lugar de usar los formularios html que bastante frecuentemente NO ME FUNCIONAN
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Reply)