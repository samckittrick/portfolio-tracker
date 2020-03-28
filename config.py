#
# Object for reading and managing configuration files.
#
import os

# Here we would add objects for reading configuration files.
class Config:
    def __init__(self):
        self.configValues = dict()
        for v in os.environ:
            self.configValues[v] = os.environ[v]

        celery_broker_url = 'redis://%s:6379/0' % (self.configValues['REDIS_HOSTNAME'])
        celery_result_backend = celery_broker_url

        self.configValues['celery_broker_url'] = celery_broker_url
        self.configValues['celery_result_backend'] = celery_result_backend

    def get_all(self):
        return self.configValues

    def get(self, config_item):
        return self.configValues[config_item]

config = Config()
