from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self,
                    username: str,
                    password: str,
                    is_staff=False,
                    is_superuser=True,
                    **extra_fields

                    ) -> "AuthUser":
        if not username:
            raise ValueError("User must have an email")

        users = self.model(username=username, **extra_fields)
        hashed_password = make_password(password)
        users.password = hashed_password
        users.is_active = True
        users.is_staff = is_staff
        users.is_superuser = is_superuser
        users.save()

        return users


class Organisation(models.Model):
    id = models.CharField(primary_key=True, max_length=100,blank=False,null=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'organisation'


class CryptoPriceModel(models.Model):
    price_id = models.AutoField(primary_key=True)
    org_id = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'crypto_price_model'


class AuthUser(AbstractUser):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField(auto_now=True)
    org = models.ForeignKey('Organisation', models.DO_NOTHING, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["id"]
    class Meta:
        managed = False
        db_table = 'auth_user'






