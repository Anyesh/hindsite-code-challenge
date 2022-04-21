from uuid import uuid4

from django.db import models

from account.models import User
from organization.models import Organization


class Post(models.Model):
    id = models.CharField(
        unique=True, max_length=120, default=uuid4, primary_key=True, editable=False
    )
    user_id = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    organization_id = models.ForeignKey(
        Organization, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    description = models.TextField(blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"POST <{self.id}>"

    class Meta:
        db_table = "Post"

        def __str__(self):
            return f"{self.__class__.__name__}: {self.name}"
