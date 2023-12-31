from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Bookstore(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bookstores_detail', kwargs={'pk': self.id})


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    # Many to Many:
    bookstores = models.ManyToManyField(Bookstore)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for book_id: {self.book_id} @{self.url}'
    

# a tuple of tuples for our ratings
RATINGS = (
    ('5', "5 Stars"),
    ('4', "4 Stars"),
    ('3', "3 Stars"),
    ('2', "2 Stars"),
    ('1', "1 Star"),
)

class Review(models.Model):
    date = models.DateField()
    finished = models.BooleanField(
        default=False,
    )
    rating = models.CharField(
        max_length=1,
        choices = RATINGS,
        default=RATINGS[0][0],
        )
    review = models.CharField(max_length=250)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_rating_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']