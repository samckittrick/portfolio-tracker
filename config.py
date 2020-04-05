#
# Object for reading and managing configuration files.
#
import os
import yaml

# Here we would add objects for reading configuration files.
class Config:
    """
    This config object can read from a file and from environment variables as well as a function for adding custom configs.
    The environment variables will override the config file and both will be overriden by the config function.

    The only way I could see to get a filename for a config file into here is through an environment variable.
    We look for the name PTAPP_CONFIG set to a path

    Example Yaml file:
        redis:
          hostname: 192.168.0.250
          port: 6379
          databaseId: 0

        influxdb:
          hostname: 192.168.0.250
          port: 8086
          databaseName: stockticker

        mariadb:
          hostname: 192.168.0.250
          port: 3306
          username: stocksdb_user
          password: stocksdb_password
          database: stocksdb


    Supported Environment Variables:
    PTAPP_REDIS_HOSTNAME - Hostname of the redis instance
    PTAPP_REDIS_PORT - port that the redis instance is listening on
    PTAPP_REDIS_DBID - database id to use in the redis database
    PTAPP_INFLUXDB_HOSTNAME - hostname of the influxdb database
    PTAPP_INFLUXDB_PORT - port for accessing the influxdb database
    PTAPP_INFLUXDB_DBNAME - the name of the influxdb database
    PTAPP_MYSQL_HOSTNAME - The hostname of the mariadb instance
    PTAPP_MYSQL_PORT - The port of the mariadb instance
    PTAPP_MYSQL_USERNAME - The username for the mariadb instance
    PTAPP_MYSQL_PASSWORD - The password for the mariadb instance
    PTAPP_MYSQL_DATABASE - The database name for the mariadb instance


    """
    def __init__(self):

        self.configValues = dict()

        if("PTAPP_CONFIG" in os.environ.keys()):
            self.readConfigFile(os.environ['PTAPP_CONFIG'])

        self.readEnvironment()

        self.generateDerivedConfiguration()

    #---------------------------------------------------------------------
    def get_all(self):
        """ Get all the configuration items """
        return self.configValues

    #-------------------------------------------------------------------
    def get(self, config_item):
        """ Get a specific config item """
        return self.configValues[config_item]

    #-------------------------------------------------------------------
    def setConfig(self, config_item, value):
        """Set a config item to a specific value"""
        self.configValues[config_item] = value

        #Regenerate the derived items.
        self.generateDerivedConfiguration()

    #------------------------------------------------------------------
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

            if('mariadb' in configs.keys()):
                r = configs['mariadb']
                self.configValues['mysql_hostname'] = r['hostname']
                self.configValues['mysql_port'] = r['port']
                self.configValues['mysql_username'] = r['username']
                self.configValues['mysql_password'] = r['password']
                self.configValues['mysql_database'] = r['database']

    #-------------------------------------------------------------------------
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
            elif(v == "PTAPP_MYSQL_HOSTNAME"):
                self.configValues['mysql_hostname'] = os.environ[v]
            elif(v == "PTAPP_MYSQL_PORT"):
                self.configValues['mysql_port'] = os.environ[v]
            elif(v == "PTAPP_MYSQL_USERNAME"):
                self.configValues['mysql_username'] = os.environ[v]
            elif(v == "PTAPP_MYSQL_PASSWORD"):
                self.configValues['mysql_password'] = os.environ[v]
            elif(v == "PTAPP_MYSQL_DATABASE"):
                self.configValues['mysql_database'] = os.environ[v]

    #---------------------------------------------------------------------------
    def generateDerivedConfiguration(self):
        """ Generate some configuration items to be read by other services"""
        redisUrl = 'redis://%s:%s/%s' % (self.configValues['redis_hostname'], self.configValues['redis_port'], self.configValues['redis_dbid'])

        self.configValues['broker_url'] = redisUrl
        self.configValues['result_backend'] = redisUrl
