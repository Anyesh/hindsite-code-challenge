from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from organization.models import Organization


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates a hindsite user with the given fields
        """

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        unique=True, max_length=120, default=uuid4, primary_key=True, editable=False
    )

    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)

    USERNAME_FIELD = "email"

    password = models.CharField(max_length=20)

    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True
    )

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    @property
    def organization_id(self):
        return self.organization.id or None

    def __str__(self):

        return f"USR <{self.email}>"

    class Meta:
        db_table = "User"

        def __str__(self):
            return f"{self.__class__.__name__}: {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"USR <{self.user.email}> "

    class Meta:
        db_table = "Profile"

        def __str__(self):
            return f"{self.__class__.__name__}: {self.name}"
