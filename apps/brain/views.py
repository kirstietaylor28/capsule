# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.db.models import Sum
import decimal 

from .models import Hat, Address, User, Measurement, Hat_Order, Order


def home(request):
    return render(request, 'brain/home.html')


def user_page(request):
    id = request.session['id']
    context = {
        "user": User.objects.filter(id=id),
        "measurement": Measurement.objects.all()
    }
    return render(request, 'brain/user_page.html', context)


def shop(request):
    return render(request, 'brain/shop.html')


def contact(request):
    form_class = ContactForm

    context = {
        'form': form_class,
    }

    if request.method == 'POST':

        form1 = form_class(request.POST)

        if form1.is_valid():
            contact_name = form1.cleaned_data.get("contact_name")
            contact_email = form1.cleaned_data.get("contact_email")
            form_content = form1.cleaned_data.get("content")
            subject = 'Site Contact Form'
            contact_message = """
            Customer Name: {},  
            \n {} 
            <Customer Email: {}>  
            """.format(contact_name, form_content, contact_email)
            from_email = settings.EMAIL_HOST_USER
            to_list = [contact_email, from_email]

            send_mail(
                subject,
                contact_message,
                from_email,
                to_list,
                fail_silently=True
            )
    return render(request, 'brain/contact.html', context)


def login(request):
    return render(request, 'brain/login.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
        if len(errors) == 0:
            user = User.objects.filter(username=request.POST['username'])
            request.session['id'] = user[0].id
            return redirect('/users')
        return redirect('/login')
    # return render(request, 'brain/signup.html')


def shopping_cart(request):
    total = Hat_Order.objects.filter(user=User.objects.get(id=request.session['id'])).aggregate(Sum('total'))
    print(total['total__sum'])
    if total['total__sum'] == None: 
        context = {
            'hat_order': Hat_Order.objects.filter(user=User.objects.get(id=request.session['id'])),
            'total' : 0,
            'grand_total' : 0,
            
        }
        return render(request, 'brain/basket.html', context)
    else: 
        context = {
            'hat_order': Hat_Order.objects.filter(user=User.objects.get(id=request.session['id'])),
            'total' : total,
            'grand_total' : total['total__sum'] + 10,
            
        }

        return render(request, 'brain/basket.html', context)


def checkout1(request):
    return render(request, 'brain/checkout.html')


def checkout2(request):
    return render(request, 'brain/checkout2.html')


def checkout3(request):
    return render(request, 'brain/checkout3.html')


def checkout4(request):

    context = {
        'hat_order': Hat_Order.objects.filter(user=User.objects.get(id=request.session['id'])),
        
    }
    return render(request, 'brain/checkout4.html', context)

def style(request, id):
    my_hat = Hat.objects.filter(id=id)
    hat = {
        'hat': my_hat,
    }
    # my_hat = Hat.objects.filter(id=id)
    request.session['hat'] = my_hat[0].id
    return render(request, 'brain/1.html', hat)


def add_cart(request):
    if request.method == "POST":
        idnum = request.session['id']
        hatnum = request.session['hat']
        my_user = User.objects.get(id=idnum)
        my_hat = Hat.objects.get(id=hatnum)
        # print my_hat
        color = request.POST['color']
        quantity = request.POST['quantity']
        brim_curvature = request.POST.get('brim', False)
        price =  Hat.objects.get(id=hatnum).price
        print (quantity)
        print (price)
        total = price * decimal.Decimal(quantity)
        print (total)
        Hat_Order.objects.create(user=my_user, hat=my_hat, color=color,
                                 quantity=quantity, brim_curvature=brim_curvature, total= total)

        return redirect("/shopping_cart")


def update_info(request):
    # my_user = User.objects.get(id=request.session['id']
    circumference = request.POST['Circumference']
    diameter_length = request.POST['Diameter_Length']
    diameter_width = request.POST['Diameter_Width']
    side_height_front = request.POST['Side_Height_Front']
    side_height_middle = request.POST['Side_Height_Middle']
    side_height_back = request.POST['Side_Height_Back']
    front_height = request.POST['Front_Height']
    brim_length = request.POST['Brim_Length']
    brim_width = request.POST['Brim_Width']
    if Measurement.objects.get(user=User.objects.get(id=request.session['id'])):
        info = Measurement.objects.update(user=User.objects.get(id=request.session['id']), circumference=circumference, diameter_length=diameter_length, diameter_width=diameter_width,
                                      side_height_front=side_height_front, side_height_middle=side_height_middle, side_height_back=side_height_back, front_height=front_height, brim_length=brim_length, brim_width=brim_width)
    else:
        info = Measurement.objects.create(user=User.objects.get(id=request.session['id']), circumference=circumference, diameter_length=diameter_length, diameter_width=diameter_width,
                                      side_height_front=side_height_front, side_height_middle=side_height_middle, side_height_back=side_height_back, front_height=front_height, brim_length=brim_length, brim_width=brim_width)
    # request.session['measurement'] = info[0].id

    context = {
        'info': info
    }
    return redirect('/users', context)

def delete(request, id):
    Hat_Order.objects.filter(id=id).delete()
    return redirect('/shopping_cart')
