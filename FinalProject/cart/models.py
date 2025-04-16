from django.db import models
from django.contrib.auth.models import User
from home.models import Vinyl

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.vinyl.title} x{self.user.username} ({self.user.username})"