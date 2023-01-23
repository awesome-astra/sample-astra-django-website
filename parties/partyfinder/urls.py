from django.urls import path

from . import views

app_name = 'partyfinder'
urlpatterns = [
  path('', views.index, name='index'),
  path('list/<str:city>/', views.parties, name='parties'),
  path('new/', views.new_party, name='new_party'),
  path('detail/<str:city>/<str:id>', views.party, name='party'),
  path('delete/<str:city>/<str:id>', views.delete_party, name='delete_party'),
]
