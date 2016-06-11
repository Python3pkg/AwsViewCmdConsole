import os
import json
from os.path import expanduser
from ConfigParser import ConfigParser
from boto3.session import Session

class AwsConnectionConfig():
    # Home directory of the user. This will ensure all platforms are fine
    home = expanduser("~")
    # Cred file location
    cred = home + '/.aws/credentials'
    __token = None
    region = None
 
    def __init__(self, awsAccId=None):
        self.awsAccId = awsAccId

        if self.awsAccId == None:
            self.awsAccId = 'default'
    
        self.__config = ConfigParser()
        self.__config.read(self.cred)

        if self.__config.has_option(self.awsAccId, "aws_session_token"):
            self.__token = self.__config.get(self.awsAccId, "aws_session_token")

        if self.__config.has_option(self.awsAccId, "region_name"):
            self.__region = self.__config.get(self.awsAccId, "region_name")
        else:
            self.region = 'us-west-2'

        self.session = Session(aws_access_key_id=self.__config.get(self.awsAccId, "aws_access_key_id"),
                            aws_secret_access_key=self.__config.get(self.awsAccId, "aws_secret_access_key"),
                            aws_session_token=self.__token,
                            region_name=self.region)
