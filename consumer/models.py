from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Address(models.Model):
    door_no = models.CharField(max_length=10, null=False)
    street = models.CharField(max_length=50, null=False)
    area = models.TextField(null=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    pincode = models.CharField(max_length=6, null=False, blank=False)


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return str(self.user.first_name)


class Subscription(models.Model):
    choices = (('1', "500ml"), ('2', "1000ml"))
    user = models.OneToOneField(Consumer, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    milk_choices = models.CharField(choices=choices, default='1', max_length=1)

    def __str__(self):
        return str(self.user.user.first_name + "---" + self.user.phone)
