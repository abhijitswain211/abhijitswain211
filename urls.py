from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('index.html', views.home, name='home'),
    path('', views.home, name="home"),
    path('shopnow.html', views.shopnow, name='shopnow'),
    path('shopnow/', views.shopnow, name='shopnow'),
    path('shop-now.html', views.shopnow, name='shopnow'),
    path('contactus', views.contactus, name="contactus"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
   

]
    
