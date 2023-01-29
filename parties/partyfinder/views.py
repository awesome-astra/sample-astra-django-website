import uuid
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.db import connection

from .models import Party
from .forms import PartyForm, CityForm

# Create your views here.
def index(request):
  if request.method == 'POST':
    form = CityForm(request.POST)
    if form.is_valid():
      return HttpResponseRedirect(reverse(
        'partyfinder:parties',
        kwargs={
          'city': form.cleaned_data['city'],
        },
      ))
    else:
      return HttpResponseRedirect(reverse('partyfinder:index'))
  else:
    form = CityForm()
  return render(
    request,
    'partyfinder/index.html',
    context={
      'form': form,
    },
  )

def party(request, city, id):
  # are we here with a "could not update 'people'" message to display?
  lwt_failed = request.GET.get('LWT_FAILED', False)
  #
  parties = Party.objects.filter(city=city, id=id)
  if len(parties)> 0:
    party = parties[0]
    context = {
      'party': party,
      'lwt_failed': lwt_failed,
    }
    return render(
      request,
      'partyfinder/party.html',
      context,
    )
  else:
    raise Http404

def parties(request, city):
  parties = Party.objects.filter(city=city).order_by('-date')
  context = {
    'city': city,
    'parties': parties,
  }
  
  return render(
    request,
    'partyfinder/list.html',
    context,
  )

def new_party(request):
  if request.method == 'POST':
    form = PartyForm(request.POST)
    if form.is_valid():
      #
      party = Party(
        **form.cleaned_data,
      )
      party.save()
      #
      return HttpResponseRedirect(reverse(
        'partyfinder:parties',
        kwargs={
          'city': form.cleaned_data['city'],
        },
      ))
  else:
    default_city = request.GET.get('city')
    f_initial = {}
    if default_city is not None:
      f_initial['city'] = default_city
    f_initial['date'] = datetime.datetime.now()
    f_initial['people'] = 0
    #
    form = PartyForm(initial=f_initial)
  return render(
    request,
    'partyfinder/new_party.html',
    {
      'form': form,
    }
  )

def delete_party(request, city, id):
  parties = Party.objects.filter(city=city, id=id)
  if len(parties)> 0:
    party = parties[0]
    city = party.city
    party.delete()
    return HttpResponseRedirect(reverse(
      'partyfinder:parties',
      kwargs={
        'city': city,
      },
    ))
  else:
    raise Http404

def change_party_people(request, city, id, prev_value, delta):
  # A LWT is a way to ensure no surprising race conditions:
  # we can ensure the provided prev_value still matches the column
  delta_num = int(delta)
  #
  cursor = connection.cursor()
  change_applied = cursor.execute(
    'UPDATE party SET people = %s WHERE city=%s AND id=%s IF people = %s',
    (
      delta_num + prev_value,
      city,
      uuid.UUID(id),  # must respect Cassandra type system
      prev_value,
    ),
  ).one()['[applied]']
  if not change_applied:
    lwt_message = '?LWT_FAILED=1'
  else:
    lwt_message = ''
  #
  return HttpResponseRedirect(reverse(
    'partyfinder:party',
    kwargs={
      'city': city,
      'id': id,
    },
  ) + lwt_message)
