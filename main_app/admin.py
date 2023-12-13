from django.contrib import admin

# import your models here.
from .models import Book
from .models import Review
from .models import Bookstore

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Bookstore)