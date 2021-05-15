from django.contrib import admin

from .models import Consumer, Address, Subscription

# Register your models here.
admin.site.register(Consumer)
admin.site.register(Address)
admin.site.register(Subscription)
