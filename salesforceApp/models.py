from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    instance_url=models.CharField(max_length=255)
    access_token=models.CharField(max_length=255)


class UserData(models.Model):
    user_id = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=20, null=True)
    phone_no = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    isactive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AccountData(models.Model):
    account_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=30, null=True)
    photourl = models.URLField(null=True)
    billingaddress = models.CharField(max_length=30, null=True)
    account_number = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class ContactData(models.Model):
    contact_id = models.CharField(max_length=255, null=True)
    accountid = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=60, null=True)
    mailingstreet = models.CharField(max_length=30, null=True)
    phone_no = models.CharField(max_length=30, null=True)
    birth_day = models.DateTimeField(null=True)
    lead_source = models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True)
    department = models.CharField(max_length=30, null=True)
    photourl = models.URLField(null=True)

    def __str__(self):
        return self.name

