from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('processregister', views.processnewuser),
    path('processlogin', views.login),
    path('welcome', views.welcome),
    path('logout', views.logout),
    path('addsong', views.addsong),
    path('processsong', views.processsong),
    path('createplaylist', views.createplaylist),
    path('processplaylist', views.processplaylist),
    path('addsongstoplaylist', views.addsongstoplaylist),
    path('seeplaylists', views.seeplaylists),
    path('displayplaylist/<int:playlistId>', views.displayplaylist),
    path('delete', views.delete),
    path('deleteplaylist', views.deleteplaylist)

]