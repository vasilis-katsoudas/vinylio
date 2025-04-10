from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vinyl(models.Model):
    GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('jazz', 'Jazz'),
        ('classical', 'Classical'),
        ('hiphop', 'Hip-Hop'),
        ('metal', 'Metal'),
        ('blues', 'Blues'),
        ('electronic', 'Electronic'),
    ]
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='vinyl_images/')
    description = models.TextField()
    release_date = models.DateField()

    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='pop')

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vinyl')

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.vinyl.title}"
