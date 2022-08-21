# Coderhouse, curso de python #31085
## Entrega final


### Revisiones:
* [x] Herencia en los templates // Implementado, hay un master.html que contiene el header, los mensajes, el explorador de categorias superior y los sitelinks. Todo lo demas se maneja a traves del block content.
* [x] manage.py duplicado
* [x] Clases basadas en vistas y mixin // Implementado, ahora el path /about/ es una clase basada en vista. (porque ese era el ejemplo en la documentacion de django, jeje.) sigo sin saber que es un mixin
* [x] Advertencia de que no existen categorías cuando recién arrancas la app sin db // Lo agregué, pero igual para evitar problemas le puse a la vista del index que si no encuentra al menos una categoría cree una por defecto, por lo que en teoría jamás deberías ver la advertencia.
* [x] RichTextBox con ckeditor // hecho
* [x] Nombre corto de las categorías como unique
* [ ] App de accounts
* [ ] Mail al registro
* [ ] Perfil de usuario con nombre, avatar, descripcion, link a una pagina, email.
* [ ] Acceso a una pantalla para que el usuario pueda modificar su informacion. Esta debe permitir modificar los datos nombrados en el punto anterior y, ademas, el password. 
* [ ] Mensajería 


### Consignas:

* [x] Link en github
* [x] README.md con ubicacion de funcionalidades o pasos a seguir para probar las cosas y los nombres de los integrantes del grupo
* [x] Nombre del repo "Entrega1+Apellidos"
* [x] Video explicativo de 10 min max (subido en el proyecto o cargado el link al mismo)
* [x] Herencia implementada en los templates
* [x] .gitignore con venv, pycache, .sqlite3, media/
* [x] Existencia del archivo requirements.txt actualizado
* [x] Rama principal main
* [x] Estructura de los archivos del proyecto:
    * accounts
    * inicio
    * mensajeria(?)
    * carpeta de configuraciones
    * templates
    * manage.py
    * gitignore
    * venv
    * db.sqlite3
    * requirements.txt
* [x] Clases definidas con PascalCase y funciones, paths, esas cosas con snake_case
* [x] Uso de un mismo idioma en todo el proyecto
* [x] Borrar todo codigo que no este en uso (imports, comments innecesarios)
* [x] No dejar botones y accesos sin funcionalidad
* [x] Minimo dos clases basadas en vista
* [x] Uso de minimo un mixin en una CBV y un decorador en una view comun
* [x] Adaptar template y vista cuando manejemos imagenes
* [x] Un home
* [x] Un 'acerca de nosotros' en el path 'about/'
* [x] 1 clase de post/blog/page con titulo, subtitulo, contenido // falta subtitulo
* [x] Acceso a una vista de listado de objetos con info minima de cada uno y que contenga un buscado por el titulo
* [x] En el listado deberia aparecer un cartel que diga que no hay objetos creados o que la busqueda no encontro ningun resultado con los datos proporcionados
* [x] Accesos a vistas para poder crear, editar y borrar un objeto.
* [x] Acceso desde el listado a cada post para ver la info completa del mismo
* [x] Tener una app "accounts" para manejar las vistas relacionadas a los usuarios // Lo manejo desde la app principal
* [x] Acceso a una pantalla de registro donde se solicite usuario, email y contraseña // no pido mail POR DISEÑO
* [x] Acceso a una pantalla de login
* [x] Acceso a una pantalla de perfil donde se muestre la informacion del usuario c/ nombre, avatar, descripcion, 1 link, email
* [x] Acceso a una pantalla para que el usuario pueda modificar su informacion
* [x] Apartado admin/ con toda la configuracion posible desde este apartado
* [ ] App de mensajeria entre usuarios
* [ ] Probar antes de hacer commits y no subir boludeces a github // fallé tremendamente en este

# Cómo testear el proyecto:
* Clonar el repositorio
* Instalar las dependencias dentro de un entorno virtual con 'pip install -r requirements.txt'
* Crear una cuenta de usuario con 'python manage.py createsuperuser'
* Iniciar el servidor con 'python manage.py runserver'
    * Dentro del panel de administrador, crear como mínimo, una categoría con nombre, nombre corto y descripcion. Opcionalmente crear una segunda categoría para testear el flag 'nsfw'
    * Estando logueado, crear un post con titulo, contenido, imagen y categoria
    * Ver la categoría dentro de la que se creo el post
    * Ver el post dentro de la categoria, actualizar el post para incrementar el contador de visitas
    * Responder al post con un comentario, ver cómo se incrementa el contador de comentarios
    * Ver el apartado 'my profile'
    * Ver el apartado 'settings', testear sus funcionalidades (cambiar usuario, cambiar contraseña, eliminar todos los posts, eliminar cuenta)
    * Teniendo todavía posts en la db, ver el apartado 'search' y buscarlos ó por una palabra del título, o de su contenido, o el nombre de usuario público de quien lo haya creado
* Opcionalmente, testear las funcionalidades de posteo y búsqueda estando deslogueado
    * Ver cómo los posts carecen de botón para editar o para eliminar
    * Intentar editar o eliminar un post que no sea suyo 'delete/<int:post_id>' ó 'edit/<int:post_id>'
    * Si la creamos, intentar ver una categoría 'nsfw'. La app redirecciona al login sin hacer uso de decoradores
    * Testear las pantallas de registro y login

### [Video explicativo](https://youtu.be/GfMHgp4lrAY)
