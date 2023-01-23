from django.contrib import admin

from .models import Party

# Making model quickly inspected and operated in the admin panel:
admin.site.register(Party)
