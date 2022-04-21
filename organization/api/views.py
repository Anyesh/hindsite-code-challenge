from rest_framework import generics
from rest_framework.permissions import AllowAny

from organization.api.serializers import OrganizationSerializer
from organization.models import Organization


class OrganizationList(generics.ListAPIView):
    queryset = Organization.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrganizationSerializer
