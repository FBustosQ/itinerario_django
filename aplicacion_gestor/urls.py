from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear/', views.crear, name='crear'),
    path('detalle/<int:id>/', views.detalle, name='detalle')
]