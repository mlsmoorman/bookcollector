from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})