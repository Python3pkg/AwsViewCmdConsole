AwsViewCmdConsole
=================

It lists the resources in an AWS account in a tabular format. The default aws credentials file must be configured
in ~/.aws/credentials as below:

*[awstestaccount]*__
*aws_access_key_id = ABCDEFGHIJKLMNOPQRSTQ*__
*aws_secret_access_key = ksgdflkagsK86875MDNkSHk<NSDlnlkfdhlskjdl;adf*__


What you need to run the tool?
-----------------------------

You need python 2.6 or 2.7, boto3 and prettytable

To install AwsViewCmdConsole, run:

pip install AwsViewCmdConsole

To run the tool, use the below command:

awslist.py -n awstestaccount -d table --list all