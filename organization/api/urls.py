from django.urls import path

from organization.api.views import OrganizationList

urlpatterns = [
    path("organizations/", OrganizationList.as_view(), name="organizations"),
]
