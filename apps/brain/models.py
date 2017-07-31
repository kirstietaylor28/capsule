from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')


class UserManager(models.Manager):

    # ---------------------------
    #    Registration Validator
    # ---------------------------

    def validate(self, post):
        errors = []

# Checking Username:
        if len(post['username']) < 2:
            errors.append('Please enter a username')
# Checking EMAIL
        if len(post['email']) <= 0:
            errors.append('Please enter an email')
        if not EMAIL_REGEX.match(post['email']):
            errors.append('Email is not in valid format')
        if self.filter(email=post['email']):
            errors.append('Email already exists in the database.')

        if self.filter(username=post['username']):
            errors.append('Username already exists in the database.')

# Checking PASSWORD

        if len(post['password']) < 8:
            errors.append('Password must contain more than 8 characters')
        if post['password'] != post['pconfirm']:
            errors.append('Please enter the same password')

# IF no errors, encrpyt password and create user
        if errors == []:
            hashed_pass = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
            User.objects.create(
                username=post['username'], email=post['email'], password=hashed_pass)
        return errors

    def login(self, post):
        errors = []
        user = User.objects.filter(username=post['username'])
        # if username is found in db
        if len(post['password']) < 2:
            errors.append("Password must be more than 2 characters long")
        if user:
            form_pw = post['password'].encode()
            db_pw = user[0].password.encode()
            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('Please enter a valid username')
        return errors


class User(models.Model):
    username = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name="Address")
    street_address = models.CharField(max_length=55)
    Street_address2 = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    zipcode = models.IntegerField()


class Measurement(models.Model):
    user = models.ForeignKey(User, related_name="Measurement")
    circumference = models.IntegerField(default=0)
    diameter_length = models.CharField(max_length=55)
    diameter_width = models.CharField(max_length=55)
    side_height_front = models.CharField(max_length=55)
    side_height_middle = models.CharField(max_length=55)
    side_height_back = models.CharField(max_length=55)
    front_height = models.CharField(max_length=55)
    brim_length = models.CharField(max_length=55)
    brim_width = models.CharField(max_length=55)


class Hat(models.Model):
    style = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Hat_Order(models.Model):
    user = models.ForeignKey(User, related_name="Hat_Order")
    hat = models.ForeignKey(Hat, related_name="the_hat")
    color = models.CharField(max_length=20)
    quantity = models.IntegerField()
    brim_curvature = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, related_name="Order")
    hat_choice = models.ManyToManyField(Hat)
    total = models.IntegerField()
    tax = models.IntegerField()
    shipping_choice = models.IntegerField()
    shipping_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
