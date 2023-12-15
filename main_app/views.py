from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Bookstore, Photo
from .forms import ReviewForm

import boto3
import uuid
import os


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)

@login_required
def add_photo(request, book_id):
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        key = f"bookcollector/{uuid.uuid4().hex[:6]}{photo_file.name[photo_file.name.rfind('.'):]}"
        try:
            bucket = os.environ["BUCKET_NAME"]
            s3.upload_fileobj(photo_file, bucket, key)
            photo_url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=photo_url, book_id=book_id)
        except Exception as e:
            print("An error uploading to AWS")
            print(e)
    return redirect("detail", book_id=book_id)


# Bookstore Associate/Unassociate Views:
@login_required
def assoc_bookstore(request, book_id, bookstore_id):
    book = Book.objects.get(id=book_id)
    book.bookstores.add(bookstore_id)
    return redirect("detail", book_id=book_id)

@login_required
def unassoc_bookstore(request, book_id, bookstore_id):
    book = Book.objects.get(id=book_id)
    book.bookstores.remove(bookstore_id)
    return redirect("detail", book_id=book_id)


# Create Class Based Views (CBV's) for Books:
class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["name", "author", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["author", "description"]


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = "/books"


# Create Class Based Views (CBV's) for Bookstores:
class BookstoreList(LoginRequiredMixin, ListView):
    model = Bookstore


class BookstoreDetail(LoginRequiredMixin, DetailView):
    model = Bookstore


class BookstoreCreate(LoginRequiredMixin, CreateView):
    model = Bookstore
    fields = "__all__"


class BookstoreUpdate(LoginRequiredMixin, UpdateView):
    model = Bookstore
    fields = "__all__"


class BookstoreDelete(LoginRequiredMixin, DeleteView):
    model = Bookstore
    success_url = "/bookstores/"


# Base views:
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")

@login_required
def books_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "books/index.html", {"books": books})

@login_required
def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    id_list = book.bookstores.all().values_list("id")
    bookstores_books_doesnt_have = Bookstore.objects.exclude(id__in=id_list)
    review_form = ReviewForm()
    return render(
        request,
        "books/detail.html",
        {
            "book": book,
            "review_form": review_form,
            "bookstores": bookstores_books_doesnt_have,
        },
    )


# Review view:
@login_required
def add_review(request, book_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.book_id = book_id
        new_review.save()
    return redirect("detail", book_id=book_id)
