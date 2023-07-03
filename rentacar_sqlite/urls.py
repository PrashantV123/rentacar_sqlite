"""rentacar_sqlite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sitemain import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('fleet', views.fleet, name='fleet'),
    path('promotion', views.promotion, name='promotion'),
    path('pricing', views.pricing, name='pricing'),
    path('protection', views.protection, name='protection'),
    path('longterm', views.longterm, name='longterm'),
    path('dealer_signup', views.dealer_signup, name='dealer_signup'),
    path('customer_signup', views.customer_signup, name='customer_signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),

    # customer
    path('reservation_request', views.reservation_request,
         name='reservation_request'),
    path('addreservation/<int:id>/<str:pd>/<str:rd>/<str:pl>/<str:rl>/<str:ty>', views.addreservation,
         name='addreservation'),
    path('showreservation', views.showreservation,
         name='showreservation'),
    path('deletereservation/<int:id>/', views.deletereservation,
         name='deletereservation'),
    path('payreservation/<int:id>/', views.payreservation,
         name='payreservation'),

    # dealer
    path('dealerdashboard', views.dealerdashboard, name='dealerdashboard'),
    path('editvehicle/<int:id>/', views.editvehicle, name='editvehicle'),
    path('deletevehicle/<int:id>/', views.deletevehicle, name='deletevehicle'),
    path('returnvehicle/<int:id>/', views.returnvehicle, name='returnvehicle'),
    path('dealerreservation', views.dealer_reservation, name='dealerreservation'),


]
