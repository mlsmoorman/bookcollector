from django.shortcuts import render
from .models import Book

# books = [
#     {'name': "Beginner's Step-By-Step Coding Course", 'author': 'DK', 'description': "Written by a team of expert coders and coding teachers, Beginner's Step-by-Step Coding Course is the ideal way to get to set you on the road to code."},
#     {'name': "Everything You Need to ACE Computer Science and Coding", 'author': 'Workman Publishing', 'description': "This Big Fat Notebook makes it all “sink in” with key concepts, mnemonic devices, definitions, diagrams, and doodles to help you understand computer science."},
# ]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def books_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})

def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/detail.html', {'book': book})