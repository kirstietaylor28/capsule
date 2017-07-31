from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    url(r'^users/$', views.user_page, name='user_page'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^shopping_cart/$', views.shopping_cart, name='shopping_cart'),
    url(r'^checkout/1$', views.checkout1, name='checkout'),
    url(r'^checkout/2$', views.checkout2, name='checkout2'),
    url(r'^checkout/3$', views.checkout3, name='checkout3'),
    url(r'^checkout/4$', views.checkout4, name='checkout4'),
    url(r'^hat/(?P<id>\d+)$', views.style, name='style'),
    url(r'^add_cart/$', views.add_cart, name='add_cart'),
    url(r'^update_info/$', views.update_info, name='update_info'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),

]
