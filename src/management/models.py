from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, EmailValidator



# Create your models here.
class CommonInfo(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        db_table = 'users'
        app_label = 'management'
        ordering = ['-updated']

    phone_regex = RegexValidator(regex=r"^00\d{11}$", message="Phone number must be entered in the format: '0034999999999'. Up to 13 digits allowed.")

    is_jedi = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=13, null=True )
    email = models.CharField(validators=[EmailValidator(message="Invalid Email")], blank=False, null=False, unique=True )

    def __str__(self):
        return self.username


class UserAccessToken(CommonInfo):
    class Meta:
        db_table = 'user_access_token'
        app_label = 'management'

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='useraccesstoken_user')
    token = models.CharField(max_length=50, null=False)


class Role(CommonInfo):
    class Meta:
        app_label = 'management'
        db_table = 'role'
        ordering = ['updated',]
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    # ADMIN = 1
    # STAFF = 2
    # CLIENT = 3
    # ROLE = (
    #     (ADMIN, 'Administrator'),
    #     (STAFF, 'Staff'),
    #     (CLIENT, 'Client'),
    # )
    name = models.CharField(max_length=250, null=True)
    order = models.IntegerField(default=0)


class RoleUser(CommonInfo):
    class Meta:
        app_label = 'management'
        db_table = 'role_user'
        ordering = ['updated',]

    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='roleuser_user')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, related_name='roleuser_role')
