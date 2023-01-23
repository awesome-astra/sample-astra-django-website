import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse

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
  parties = Party.objects.filter(city=city, id=id)
  if len(parties)> 0:
    party = parties[0]
    context = {
      'party': party,
    }
    print(party)
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
