from django.contrib import admin

# import your models here.
from .models import Book, Review, Bookstore, Photo

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Bookstore)
admin.site.register(Photo)