AwsViewCmdConsole
=================

It lists the resources in an AWS account in a tabular format. The default aws credentials file must be configured
in ~/.aws/credentials

What you need to run the tool?
-----------------------------

You need python 2.6 or 2.7, boto3 and prettytable

To install boto3, use the below command

pip install boto3
pip install prettytable

To run the tool, use the below command:

python ./bin/awslist.py -n kaos-test -d table --list all