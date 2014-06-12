from optparse import make_option
import csv
from bugs.models import Bugs
import datetime
 
from django.core.management.base import BaseCommand, CommandError
 
class Command(BaseCommand):
    help = 'Runs the next item in the import queue'
    option_list = BaseCommand.option_list + (
        make_option('--file',
            dest='csv_file',
            default=None,
            help='File to Ingest'),
    )
 
    def handle(self, *args, **options):
        csv_filepath = options['csv_file']
        if csv_filepath is None:
            raise CommandError('No CSV File passed')

        with open(csv_filepath, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            keys = reader.next()
            bugs = []
            date_format = '%m/%d/%Y %H:%M'

            def map_keys(keys, data):
                d={}
                for i in range(0, len(data)):
                    d[keys[i]] = data[i]
                return d

            print keys

            for entry in reader:
                #bugs.append(map_keys(keys, entry))
                mappings = map_keys(keys,entry)
                bugs.append(Bugs(
                    bug_id=mappings['Id'],
                    manager_id = mappings['Manager'],
                    entry_date = datetime.datetime.strptime(mappings['Entry Date'], date_format),
                    age = mappings['Age'],
                    status = mappings['Status'],
                    severity = mappings['Severity'],
                    product = mappings['Product'],
                    is_open = mappings['Open'],
                    month_start = mappings['Month Start']))

            Bugs.objects.bulk_create(bugs[:100])