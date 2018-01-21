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
        request.session['name']= user.name
        return redirect('/travels')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name']= login_return['user'].name
        return redirect('/travels')
    else:
        messages.error(request, login_return['errors'])
        return redirect('/')

# def success(request):
#comparing in views for post is:
#if request.method == "POST": 
    

def travels(request): #dashboarddashboard
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
   
        
    context = {
        # "trips":Trip.objects.exclude(request.session['id']),
        # "other_users": User.objects.trip.exclude(id=request.session['id']),
        # 'user': User.objects.get(id=request.session['id']),
        'user': User.objects.get(id=request.session['id']).trips.all(),



        'othertrips': Trip.objects.exclude(users=request.session['id']),


        # why does filter not wor? 
        # 'mytrips': Trip.objects.filter(id=request.session['id']),
        #exclude if travelers = session ID 
        #grab the queries the logged in user is in, and then grabbing all the ones the user is NOT in, for the 
        "users":User.objects.all(),
    }
    
    # context = {"trips":Trip.objects.get(id=user_id)}

    return render(request, 'main/travels.html', context)

def join(request, trip_id):
    a = Trip.objects.get(id=trip_id)
    User.objects.get(id=request.session['id']).trips.add(a)
    return redirect('/travels')

def add(request):
    return render(request, 'main/add.html')

def newtrip(request):
    t_errors = Trip.objects.tripvalidator(request.POST)
    if t_errors:
        for error in t_errors:
            messages.error(request, t_errors[error])
        return redirect('/add')
    else:
        trip = Trip.objects.create(desc=request.POST['desc'], dest=request.POST['dest'], travel_start=request.POST['travel_start'], travel_end=request.POST['travel_end'])
        #user = User.object.get(id=request.session['id'])
        #what is this for again? 
        return redirect('/travels')

        
def destination(request, trip_id):
    #Solutions below: 
    # trip = Trip.objects.get(id=trip_id)
    # context = {
    #     'temp.trip': trip
    # }
    # Planned by :{{temp.trip.planned_by.name}}
    #in the html, we would say {% for users in trip.travelers.all %}
    # {% user.name %}
    #filter by trip ID and display users , and if users id != session id, then display trip
    
    context = {
        'users': User.objects.all(),
        'planner': User.objects.exclude(id=request.session['id']),

        "trip": Trip.objects.filter(id=trip_id)
        #use exclude to see other users joining the trip, but you  need 1:many for the planned by 
        # "trips":Trip.objects.filter(users=User.objects.get(id=trip_id))
    }
    return render(request, 'main/destination.html', context)


def logout(request):
    del request.session['id']
    del request.session['name']
    return redirect('/')

