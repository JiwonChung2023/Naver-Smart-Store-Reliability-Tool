<<<<<<< HEAD
from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path("", views.index, name="index"),
    path("move/", views.move, name="move"),
=======
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
>>>>>>> 74da7df84f4910ad177c46656938bc1ce1afeb51
]