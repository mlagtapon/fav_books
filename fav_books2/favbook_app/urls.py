from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
    path('addbook', views.addbook),
    path('books/<int:book_id>/', views.aboutbooks), #my browser kept adding a slash
    path('books/<int:book_id>', views.aboutbooks),
    path('fav/<int:book_id>/<int:user_id>', views.fav),
    path('unfav/<int:book_id>/<int:user_id>', views.unfav),
    path('delete/<int:book_id>', views.delete),
    path('update/<int:book_id>', views.update_book)
]