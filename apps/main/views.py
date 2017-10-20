# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pw)
        request.session['id'] = user.id
        return redirect('/travels')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        # messages.success(request, "you have successfully logged in") 
        return redirect('/travels')
    else:
        messages.error(request, login_return['error'])
        return redirect('/')

def travels(request): #dashboard 
    
    # a = Trip.objects.get(id=trip_id)
    # context = {
    #     "trips":Trip.objects.get(id=trip_id)
    # }
    context = {
        "trips":Trip.objects.all(),
        "users":User.objects.all()
    }
    # context = {"trips":Trip.objects.get(id=user_id)}
    return render(request, '/main/travels.html', context)

def join(request, user_id, trip_id):
    a = Trip.objects.get(id=trip_id)
    b = User.objects.get(id=user_id)

    b.trips.add(a)
    return redirect('/travels')

def add(request):
    return render(request, 'main/add.html')

def newtrip(request):
    if request.method == "POST":
        if len(request.method['dest']) == 0 or len(request.method['desc']) == 0 or len(request.method['datefrom']) == 0 or len(request.method['dateto']) == 0:
            messages.error(request, "Cannot submit empty fields")
            return redirect('/add')
        if (request.method['dateto']) == request.method['datefrom']):
            messages.error(request, "Travel Start and End Date cannot be the same")
            return redirect('/add')
        if (request.method['dateto']) > (request.method['datefrom']):
            messages.error(request, "Travel End Date cannot be earlier than Travel To Date")
            return redirect('/add')
        else:
            return redirect('/travels')

        

def display(request, trip_id):
    context = {
        "trips":Trip.objects.filter(users=User.objects.get(id=trip_id))
    }
    return render(request, 'main/destination.html', context)

def logout(request):
    del request.session['id']
    return redirect('/')

