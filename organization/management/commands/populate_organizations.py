from django.core.management.base import BaseCommand

from organization.models import Organization

DATA = [
    Organization(name="Org1", country="Nepal", language="Nepali"),
    Organization(name="Org2", country="India", language="Hindi"),
    Organization(name="Org3", country="China", language="Chinese"),
]


class Command(BaseCommand):
    help = "Check and create user profile"

    def create_profile(self):

        return Organization.objects.bulk_create(DATA)

    def handle(self, *args, **options):
        data = self.create_profile()

        self.stdout.write(
            self.style.SUCCESS('Successfully created "%s" organizations' % len(data))
        )
