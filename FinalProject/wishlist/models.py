from django.db import models
from django.contrib.auth.models import User
from home.models import Vinyl

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.vinyl.title}"
