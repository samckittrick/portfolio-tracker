#
# Object for reading and managing configuration files.
#
import os
import yaml

# Here we would add objects for reading configuration files.
class Config:
    """
    This config object can read from a file and from environment variables.
    The environment variables will override the config file

    Example Yaml file:
        redis:
          hostname: 192.168.0.250
          port: 6379
          databaseId: 0

        influxdb:
          hostname: 192.168.0.250
          port: 8086
          databaseName: stockticker

    Supported Environment Variables:
    PTAPP_REDIS_HOSTNAME - Hostname of the redis instance
    PTAPP_REDIS_PORT - port that the redis instance is listening on
    PTAPP_REDIS_DBID - database id to use in the redis database
    """
    def __init__(self, configFile=None):

        self.configValues = dict()

        if(configFile is not None):
            self.readConfigFile(configFile)

        self.readEnvironment()

        self.generateDerivedConfiguration()

    def get_all(self):
        """ Get all the configuration items """
        return self.configValues

    def get(self, config_item):
        """ Get a specific config item """
        return self.configValues[config_item]

    def readConfigFile(self, configFile):
        """ Read config items from a yaml config file """
        with open(configFile, 'r') as cf:
            configs = yaml.load(cf, Loader=yaml.SafeLoader)

            if('redis' in configs.keys()):
                r = configs['redis']
                self.configValues['redis_hostname'] = r['hostname']
                self.configValues['redis_port'] = r['port']
                self.configValues['redis_dbid'] = r['databaseId']

            if('influxdb' in configs.keys()):
                r = configs['influxdb']
                self.configValues['influxdb_hostname'] = r['hostname']
                self.configValues['influxdb_port'] = r['port']
                self.configValues['influxdb_dbName'] = r['databaseName']

    def readEnvironment(self):
        """ Read environment variables. Definitions at the object level """

        for v  in os.environ:

            if(v == "PTAPP_REDIS_HOSTNAME"):
                self.configValues['redis_hostname'] = os.environ[v]
            elif(v == "PTAPP_REDIS_PORT"):
                self.configValues['redis_port'] = os.environ[v]
            elif(v == "PTAPP_REDIS_DBID"):
                self.configValues['redis_dbid'] = os.environ[v]
            elif(v == "PTAPP_INFLUXDB_HOSTNAME"):
                self.configValues['influxdb_hostname'] = os.environ[v]
            elif(v == "PTAPP_INFLUXDB_PORT"):
                self.configValues['influxdb_port'] = os.environ[v]
            elif(v == "PTAPP_INFLUXDB_DBNAME"):
                self.configValues['influxdb_dbName'] = os.environ[v]

    def generateDerivedConfiguration(self):
        """ Generate some configuration items to be read by other services"""
        redisUrl = 'redis://%s:%s/%s' % (self.configValues['redis_hostname'], self.configValues['redis_port'], self.configValues['redis_dbid'])

        self.configValues['broker_url'] = redisUrl
        self.configValues['result_backend'] = redisUrl
