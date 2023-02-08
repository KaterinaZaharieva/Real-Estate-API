""" import path from django and views """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('favourites',views.favourite_list, name='favourite_list'),
]
