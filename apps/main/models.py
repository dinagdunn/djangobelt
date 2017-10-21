# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt



class UserManager(models.Manager):
    def validator(self, postData): 
        errors ={}
        if len(postData['name']) < 3:
            errors['name_error'] = "Name must be 3 characters or more"
        if len(postData['username']) < 3:
            errors['name_error'] = "Username must be 3 characters or more"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_len'] = "Password must be 8 characters or more"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords do not match"
        if User.objects.filter(username=postData['username']):
            errors['exists'] = "Username has already been taken"
        return errors
       
    def login(self, postData):
        user_check = User.objects.filter(username=postData['username'])
        if len(user_check) > 0:
            user_check = user_check[0] 
            if bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
                user = {'user': user_check} 
                return user
            else:
                errors = {'errors': "Invalid Login. Please try again"}
                return errors
        else:
            errors = {'errors': "Invalid Login. Please try again"}
            return errors



class Trip(models.Model):
    dest = models.CharField(max_length = 255)
    desc = models.TextField()
    travel_start = models.DateTimeField()
    travel_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    # creator = models.ForeignKey(User,related_name="users")

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    trips = models.ManyToManyField(Trip, related_name="users")
    objects=UserManager()







