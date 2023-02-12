""" import path from django and views """
import notifications.urls
from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_single, name='post_single'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('favourites',views.favourite_list, name='favourite_list'),
    path('submit_review/<slug:post>/',views.submit_review, name='submit_review'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('<int:post_id>/inspect/',views.inspect, name='inspect'),
    path('<int:inspection_id>', views.view_inspection, name='view_inspection'),
     path('', views.notifications, name='notifications'),
]
