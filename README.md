# AwsViewCmdConsole

It lists the resources in an AWS account in a tabular format. The default aws credentials file must be configured
in ~/.aws/credentials as below:

```sh
[awstestaccount]
aws_access_key_id = ABCDEFGHIJKLMNOPQRSTQ
aws_secret_access_key = ksgdflkagsK86875MDNkSHk<NSDlnlkfdhlskjdl
```

## What you need to run the tool?

You need python 3, boto3 and prettytable

To install AwsViewCmdConsole, run:

```sh
pip3 install AwsViewCmdConsole
```

To run the tool, use the below command:

```sh
awsview -n awstestaccount -d table --list all
```
