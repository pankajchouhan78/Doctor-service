from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register_docuter/',views.register_docuter,name="register_docuter"),
    path('add_patient/',views.add_patient , name ="add_patient"),
    path('docuter/',views.docuter, name ="docuter"),
    path('donedocuter/<int:id>/',views.donedocuter, name ="donedocuter"),
]
