from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
        name = models.CharField(max_length=100)

        def __str__(self):
            return self.name

class Vinyl(models.Model):
    GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('alternative', 'Alternative'),
        ('jazz', 'Jazz'),
        ('hiphop', 'Hip-Hop'),
        ('metal', 'Metal'),
        ('rnb', 'R&B'),
        ('electronic', 'Electronic')
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='vinyl_images/')
    description = models.TextField()
    release_date = models.DateField()

    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='pop')

    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Rating(models.Model):
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1)

    class Meta:
        unique_together = ('vinyl', 'user')

class Favorite(models.Model):
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vinyl', 'user')

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'vinyl')