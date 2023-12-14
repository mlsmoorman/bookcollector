from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, Bookstore
from .forms import ReviewForm

# Bookstore Associate/Unassociate Views:
def assoc_bookstore(request, book_id, bookstore_id):
    book = Book.objects.get(id=book_id)
    book.bookstores.add(bookstore_id)
    return redirect('detail', book_id=book_id)    
    
def unassoc_bookstore(request, book_id, bookstore_id):
    book = Book.objects.get(id=book_id)
    book.bookstores.remove(bookstore_id)
    return redirect('detail', book_id=book_id)

# Create Class Based Views (CBV's) for Books:
class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['author', 'description']

class BookDelete(DeleteView):
    model = Book
    success_url = '/books'

# Create Class Based Views (CBV's) for Bookstores:
class BookstoreList(ListView):
    model = Bookstore
    
class BookstoreDetail(DetailView):
    model = Bookstore
    
class BookstoreCreate(CreateView):
    model = Bookstore
    fields = '__all__'
    
class BookstoreUpdate(UpdateView):
    model = Bookstore
    fields = '__all__'
    
class BookstoreDelete(DeleteView):
    model = Bookstore
    success_url = '/bookstores/'

# Base views:
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def books_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books':books})

def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    id_list = book.bookstores.all().values_list('id')
    bookstores_books_doesnt_have = Bookstore.objects.exclude(id__in=id_list)
    review_form = ReviewForm()
    return render(request, 'books/detail.html', {'book':book, 'review_form':review_form, 'bookstores':bookstores_books_doesnt_have})

# Review view:
def add_review(request, book_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.book_id = book_id
        new_review.save()
    return redirect('detail', book_id=book_id)

