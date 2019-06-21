from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        print(postData)
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 1:
            errors["email"] = "Email field is required!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "email be a valid email address"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['conf_pass']:
            errors['conf_pass'] = "Passwords do not match."
        return errors
    def validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['no_email'] = "Please input an email."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['email_valid'] = "Email is not valid."
        elif not User.objects.get(email=postData['email']):
            errors['email_exist'] = "This email is not registered in our database."
        if len(postData['password']) < 1:
            errors['no_pass'] = "Please input a password."
        elif len(postData['password']) < 8:
            errors['short_pass'] = "Incorrect password: less than 8 characters."
        elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
            errors['incorrect_pass'] = "Incorrect password"
        return errors
    def bookvalid(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['no_title'] = "Please input a title."
        if len(postData['desc']) < 5:
            errors['short_desc'] = "Description must be at least 5 characters."
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    #liked_books = list of books a given user likes
    #books_uploaded = list of books uploaded by a given user

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()    


