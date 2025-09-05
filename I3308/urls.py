"""
URL configuration for I3308 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from clients.views import signup_view,login_view,home_view,yoga_view,reservation_view,membership_view,membership_card_view,yoga_membership_view,gym_view,product_list,detail,cart,add_to_cart,update_cart,remove_from_cart,checkout,logout_view,swimming_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup_view,name='Sign up'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('',home_view,name='home'),
    path('swimming/',swimming_view,name='swimming'),
    path('yoga/',yoga_view,name="yoga"),
    path('reservation/',reservation_view,name='reservation'),
    path('membership/',membership_view,name='membership'),
    path('membership_card/',membership_card_view,name='membership_card'),
    path('yoga_membership/',yoga_membership_view,name='yoga_membership'),
    path('gym/',gym_view,name='gym'),   
    path('products/', product_list, name='product_list'),
    path('<int:pk>/',detail,name='detail'),
    path('cart/', cart, name='cart'),
    path('<int:pk>/', detail, name='detail'),  # Example detail view URL
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),  # URL pattern for add_to_cart view
    path('update_cart/<int:item_id>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)