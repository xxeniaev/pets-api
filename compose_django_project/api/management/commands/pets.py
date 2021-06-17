import json

from django.core.management.base import BaseCommand

from api.serializers import PetSerializer
from api.models import PetModel


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--has-photos',
            action='store_true',
            help='True if pets with photos, False if not'
        )
        parser.add_argument(
            '--no-photos',
            action='store_true',
            help='True if pets with photos, False if not'
        )

    def handle(self, *args, **options):
        qs = PetModel.objects

        if options['has_photos'] or options['no_photos']:
            if options['has_photos']:
                qs = qs.exclude(photos=None)
            elif options['no_photos']:
                qs = qs.filter(photos=None)
        else:
            qs = qs.all().order_by('id')

        serializer = PetSerializer(qs, many=True)
        serializer_data = list(serializer.data)
        response_data = {'pets': serializer_data}
        self.stdout.write(json.dumps(response_data, indent=2))
