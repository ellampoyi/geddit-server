from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from geddit.models import ListedErrand  #this path seems to be wrong cant figure out why


class Command(BaseCommand):
    help = 'Delete records older than 24 hours'

    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - timedelta(hours=24)
        ListedErrand.objects.filter(list_time__lt=time_threshold).delete()
        self.stdout.write('Old records deleted.')


'''      
this might not work as it might put too much load on django
in which case use the sql query below
CREATE EVENT delete_old_records
 ON SCHEDULE EVERY 1 HOUR
 DO
   DELETE FROM your_table
   WHERE list_time < NOW() - INTERVAL 24 HOUR;
   
before running this command, make sure to run the following command
SET GLOBAL event_scheduler = ON;
'''
