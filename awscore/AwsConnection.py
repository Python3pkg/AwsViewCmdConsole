from os.path import expanduser
from ConfigParser import ConfigParser
from boto3.session import Session


class AwsConnection(object):
    """ Home directory of the user. This will ensure all platforms are fine """
    homedir = expanduser("~")
    """ Cred file location """
    awscred = homedir + '/.aws/credentials'
    __session_token = None
    aws_region = None
    elbclient = None
    ec2client = None
    ec2resource = None
    r53client = None
    cfclient = None

    def __init__(self, awsaccno=None):
        self.awsaccno = awsaccno

        if self.awsaccno == None:
            self.awsaccno = 'default'
    
        self.__config = ConfigParser()
        self.__config.read(self.awscred)

        if self.__config.has_option(self.awsaccno, "aws_session_token"):
            self.__session_token = self.__config.get(self.awsaccno, "aws_session_token")

        if self.__config.has_option(self.awsaccno, "region_name"):
            self.aws_region = self.__config.get(self.awsaccno, "region_name")
        else:
            self.aws_region = 'us-west-2'

        self.session = Session(aws_access_key_id=self.__config.get(self.awsaccno, "aws_access_key_id"),
                            aws_secret_access_key=self.__config.get(self.awsaccno, "aws_secret_access_key"),
                            aws_session_token=self.__session_token,
                            region_name=self.aws_region)

        """ elb client """
        self.elbclient = self.session.client('elb')

        """ ec2 client """
        self.ec2client = self.session.client('ec2')

        """ ec2 resource """
        self.ec2resource = self.session.resource('ec2')

        """ route53 client """
        self.r53client = self.session.client('route53')

        """ cloudformation client """
        self.cfclient = self.session.client('cloudformation')

        """ rds client"""
        self.rdsclient = self.session.client("rds")
