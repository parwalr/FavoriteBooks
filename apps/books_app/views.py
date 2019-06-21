from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
import re

def index(request):
    if 'id' in request.session.keys():
        return redirect('/books')
    else:
        return render(request, 'books_app/login.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/books')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request,"User not recognized")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            print ('password matches')
            request.session['id'] = user[0].id
            return redirect('/books')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')

def books(request):
    if 'id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'books': Book.objects.all(),
        }
        return render (request, 'books_app/books.html', context)
    else: 
        return redirect('/')

def add_book(request):
    errors = User.objects.bookvalid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        new_book= Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=User.objects.get(id=request.session['id']))
        new_book.users_who_like.add(User.objects.get(id=request.session['id']))
        return redirect('/books')

def show_book(request, id):
    book = Book.objects.get(id=int(id))
    likers = book.users_who_like.all()
    context = {
        'book' : book,
        'user' : User.objects.get(id=request.session['id']),
        'likers': likers
    }
    return render (request, 'books_app/show.html', context)

def add_fav (request, id):
    book = Book.objects.get(id=int(id))
    user = User.objects.get(id=request.session['id'])
    book.users_who_like.add(User.objects.get(id=request.session['id']))
    return redirect ('/books')

def add_favs (request, id):
    book = Book.objects.get(id=int(id))
    user = User.objects.get(id=request.session['id'])
    book.users_who_like.add(User.objects.get(id=request.session['id']))
    return redirect ('/books/' + str(id))

def unfave (request, id):
    book = Book.objects.get(id=int(id))
    user = User.objects.get(id=request.session['id'])
    book.users_who_like.remove(user)
    return redirect ('/books/'+ str(id))

def update_info(request, id):
    book = Book.objects.get(id=int(id))
    book.title = request.POST.get('title')
    book.desc = request.POST.get('desc')
    book.save()
    return redirect('/books/' + str(book.id))

def destroy(request, id):
    Book.objects.get(id=int(id)).delete()
    return redirect('/books')

def user(request, id):
    user = User.objects.get(id=int(id))
    books = user.liked_books.all()
    context = {
        'user' : user,
        'books': books,
    }
    return render (request, 'books_app/user.html', context)

def logout(request):
    request.session.clear()
    return redirect ('/')