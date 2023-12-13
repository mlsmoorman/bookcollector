from django.shortcuts import render, redirect
# from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book
from .forms import ReviewForm

# Create Class Based Views (CBV's) here.
# class BookList(ListView):
#     model = Book

# class BookDetail(DetailView):
#     model = Book
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['book_list'] = Book.objects.all()
#         return context         

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['author', 'description']

class BookDelete(DeleteView):
    model = Book
    success_url = '/books'


# Create base views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def books_index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books':books})

def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    review_form = ReviewForm()
    return render(request, 'books/detail.html', {'book':book, 'review_form':review_form})

def add_review(request, book_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.book_id = book_id
        new_review.save()
    return redirect('detail', book_id=book_id)