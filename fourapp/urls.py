"""fourjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from fourapp import views


app_name = 'fourapp'

urlpatterns = [
    path('', views.index, name='index'), #index
    path('new_post/', views.new_post, name='new_post'), #no hay nada en el url, se usa para crear un nuevo post
    path('image/<int:image_id>', views.image, name='image'), #no hay nada en el url, se usa para mostrar una imagen
    path('view_category/<int:category_id>', views.view_category_by_id, name='view_category'), #ver la categoría por id {/view_category/1}
    path('<str:short>', views.view_category_by_short, name='view_category'), #ver la categoría por short {/sci}
    path('post/<int:post_id>', views.view_post, name='view_post'), #ver el post por id {/post/1}
    path('post/<int:post_id>/reply', views.reply, name='reply'), #crear una respuesta al post {/post/1/reply}
    path('<str:short>/post', views.post_from_category, name='post_from_category'), #crear un post directamente desde dentro de la categoria {/sci/post}
    path('edit/<int:post_id>', views.edit_post, name='edit_post'), #editar un post {/edit/1}
    path('delete/<int:post_id>', views.delete_post, name='delete_post'), #eliminar un post {/delete/1}
    path('about/', views.AboutView.as_view(), name='about'), #about {/about}
    path('search/', views.search, name='search'), #buscar un post {/search}
]
