from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.cache import cache



class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
         if not email:
            raise ValueError(_("The Email must be set"))
         email = self.normalize_email(email)
         user = self.model(email=email, **extra_fields)
         user.set_password(password)
         user.save()
         return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 'ADMIN')
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",_("Admin")
        SUBSCRIBER = 'SUBSCRIBER', _('Subscriber')
        REGULAR = 'REGULAR', _('Regular')

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.REGULAR)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_cached_role(self):
        cache_key = self.id
        role = cache.get(cache_key)
        if not role:
            role = self.role
            cache.set(cache_key,role,timeout=3600)
        return role

    @property
    def is_premium(self):
        if self.role == self.Role.ADMIN:
            return True
        return (
            self.role == self.Role.SUBSCRIBER and
            self.subscription_expires_at and
            self.subscription_expires_at > timezone.now()
            )

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='Profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="media/images/avatar/",blank=True,null=True)
    def __str__(self) -> str:
        return self.user.email
