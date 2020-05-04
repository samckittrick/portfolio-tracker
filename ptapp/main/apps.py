from django.apps import AppConfig
from django.conf import settings
from influxable import Influxable

class MainConfig(AppConfig):
    name = 'main'

    #-------------------------------------------------------------------------#
    #def ready(self):
    #    influxInstance = Influxable(base_url=settings.INFLUXDB_DATABASE['hostname'], database_name=settings.INFLUXDB_DATABASE['database'])
