from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')

    else:
        tohash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        tohashtwo = bcrypt.hashpw(request.POST['confirm'].encode(),bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=tohash, confirm=tohashtwo)

        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id
        return redirect('/books')

def login(request):

    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
	
        user = User.objects.filter(email=request.POST['email_login'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password.", extra_tags ="login")
            return redirect ('/')

        if not bcrypt.checkpw(request.POST['password_login'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password.", extra_tags ="login")
            return redirect ('/')
        
        request.session['user_id'] = user[0].id
        request.session['first_name'] = user[0].first_name
        return redirect ('/books')
        
    else: 
        return redirect('/')

def books(request):

    context = {
        'allbook': Book.objects.all(),
        'name': request.session['first_name'],
        'id': request.session['user_id']
    }

    return render(request, 'books.html', context)

def addbook(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/books')

    user_id = User.objects.get(id= request.session['user_id'])
    fav = Book.objects.create(title=request.POST['title'], desc =request.POST['desc'], uploaded_by=user_id)

    fav_id = fav.id

    the_book = Book.objects.get(id=fav_id)
    the_user = User.objects.get(id=request.session['user_id'])

    the_book.likes.add(the_user)

    return redirect('/books')

def aboutbooks(request, book_id):

    one_book = Book.objects.get(id=book_id)

    context = {
        "allbook": Book.objects.all(),
        "one_book": one_book,
        'name': request.session['first_name'],
        'id': request.session['user_id'],
    }

    return render(request, 'aboutbooks.html', context)

def fav(request, book_id, user_id):
    the_book = Book.objects.get(id=book_id)
    the_user = User.objects.get(id=request.session['user_id'])

    the_book.likes.add(the_user)
    return redirect('/books')

def unfav(request, book_id, user_id):
    the_book = Book.objects.get(id=book_id)
    the_user = User.objects.get(id=request.session['user_id'])

    the_book.likes.remove(the_user)
    
    return redirect('/books/' + str(book_id))

def update_book(request, book_id):
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect('/books/' + str(book_id))

        book_to_update = Book.objects.get(id=book_id)
        book_to_update.desc = request.POST['desc']
        book_to_update.title = request.POST['title']
        book_to_update.save()

        return redirect('/books/' + str(book_id))
    else:
        return redirect('/books')

def delete(request, book_id):
    destroy = Book.objects.get(id=book_id)
    destroy.delete()
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')
