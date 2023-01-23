from django.urls import path

from . import views

app_name = 'partyfinder'
urlpatterns = [
  path('', views.index, name='index'),
  path('list/<str:city>/', views.parties, name='parties'),
  path('new/', views.new_party, name='new_party'),
  path('detail/<str:city>/<str:id>', views.party, name='party'),
  path('delete/<str:city>/<str:id>', views.delete_party, name='delete_party'),
  path('change_people/<str:city>/<str:id>/<int:prev_value>/<str:delta>', views.change_party_people, name='change_party_people'),
  # 'delta' above is a string to allow for '-1' and '+1'
]
