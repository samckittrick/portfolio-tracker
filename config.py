#
# Object for reading and managing configuration files.
#

# Here we would add objects for reading configuration files.
class Config:
    def __init__(self):
        self.redisHostname = "localhost"
        self.CELERY_BROKER_URL = 'redis://%s:6379/0' % self.redisHostname
        self.CELERY_RESULT_BACKEND = 'redis://%s:6379/0' % self.redisHostname


config = Config()
