from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Utilizo el nombre de usuario para relacionar con la autenticación
# de django porque tuve problemas usando el id con OneToOneField.
# asi como esta ahora no deberia generar problemas, pero te limita:
# por un lado, buscar por username va a ser inherentemente mas lento
#que por id, y por otro, no te permite modificar el login sin tener que
# hacer un trigger
class UserProfile(models.Model):
    profile_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    link = models.URLField(blank=True)
    def __str__(self):
        return self.user.username