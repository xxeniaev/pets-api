import json

from django.core.management.base import BaseCommand

from compose_django_project.api.serializers import PetSerializer
from compose_django_project.api.models import PetModel


class Command(BaseCommand):
    help = 'Get list of pets filtered by having photos'

    def add_arguments(self, parser):
        # optional arguments
        parser.add_argument(
            '--has-photos', type=str, metavar='',
            help='enter True/true if pets with photos, False/false if not'
        )

    def handle(self, *args, **options):
        qs = PetModel.objects

        if options['has_photos']:
            if options['has_photos'] == "True" or options['has_photos'] == "true":
                qs = qs.exclude(photos=None)
            elif options['has_photos'] == "False" or options['has_photos'] == "false":
                qs = qs.filter(photos=None)
        else:
            qs = qs.all()

        serializer = PetSerializer(qs, many=True)
        serializer_data = list(serializer.data)
        response_data = {'pets': serializer_data}
        self.stdout.write(json.dumps(response_data, indent=2))
