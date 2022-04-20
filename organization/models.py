from uuid import uuid4

from django.db import models


class Organization(models.Model):
    id = models.CharField(
        unique=True, max_length=120, default=uuid4, primary_key=True, editable=False
    )
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    language = models.CharField(max_length=20)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ORG <{self.name}>"

    class Meta:
        db_table = "Organization"

        def __str__(self):
            return f"{self.__class__.__name__}: {self.name}"
