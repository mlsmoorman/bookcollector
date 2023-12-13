from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('books/', views.books_index, name='index'),
    
    path('books/<int:book_id>/', views.books_detail, name='detail'),
    path('books/create/', views.BookCreate.as_view(), name='books_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
	path('books/<int:book_id>/add_review/', views.add_review, name='add_review'),
    
    path('books/<int:book_id>/assoc_bookstore/<int:bookstore_id>', views.assoc_bookstore, name='assoc_bookstore'),
    path('books/<int:book_id>/unassoc_bookstore/<int:bookstore_id>', views.assoc_bookstore, name='unassoc_bookstore'),
    
    path('bookstores/', views.BookstoreList.as_view(), name='bookstores_index'),
    path('bookstores/<int:pk>/', views.BookstoreDetail.as_view(), name='bookstores_detail'),
    path('bookstores/create/', views.BookstoreCreate.as_view(), name='bookstores_create'),
    path('bookstores/<int:pk>/update/', views.BookstoreUpdate.as_view(), name='bookstores_update'),
    path('bookstores/<int:pk>/delete/', views.BookstoreDelete.as_view(), name='bookstores_delete'),
]

