#
# We use factory_boy to build test fixture models easily and quickly
#
import factory
from imports import models

import datetime

##################################################
# For creating fixtures using FileData
##################################################
class FileDataFactory(factory.Factory):
    fileid = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
    filename = "testfile.noext"
    expiration = datetime.datetime.now()

#################################################
# For creating fixtures using AccountData
#################################################
class AccountDataFactory(factory.Factory):
    file = factory.Factory.SubFactory(FileDataFactory)
    friendlyName = "testAccount"
    account_id = "1234"
    routing_number = "2345"
    institution_name = "test institution"
    institution_id = "3456"
