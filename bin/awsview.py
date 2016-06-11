import os
import sys
from argparse import ArgumentParser

from prettytable import PrettyTable

paths = []

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
for item in os.listdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))):
    if os.path.isdir(item):
        if item not in ["conf", "external", "helperscripts"]:
            path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', item))
            if path not in sys.path:
                sys.path.append(path)

from core.AwsConnectionConfig import AwsConnectionConfig


def listVpcs(awsConnConf, doption):
    # session client for ec2
    client = awsConnConf.session.client('ec2')
    # all vpc information in the region
    allVpcs = client.describe_vpcs()
    x = PrettyTable(["Vpc Id", "Name"])
    x.align["Vpc Id"] = "l"
    x.align["Name"] = "l"

    '''
    iterate over the VPCs
    '''
    print '\n'
    print '{0}'.format("\033[1m" + "VPCs in the Account" + "\033[0m")
    for vpcs in allVpcs['Vpcs']:
        if vpcs.get("Tags"):
            print vpcs["Tags"]
        x.add_row([vpcs['VpcId']])

    if doption == "table":
        print x

    elif doption == "html":
        print x.get_html_string()        


def getRoute53Records(client, doption):
    print "DNS Records(CNAMEs)"
    x = PrettyTable(["CNAME", "ELB/ILB DNS Name"])
    x.align["CNAME"] = "l"
    x.align["ELB/ILB DNS Name"] = "l"    
    for zone in client.list_hosted_zones()['HostedZones']:
        for rrsets in client.list_resource_record_sets(HostedZoneId=zone['Id'])['ResourceRecordSets']:
            for tag in ["chef", "secure", "prediction", "transformation"]:
                if tag in rrsets['Name']:
                    x.add_row([rrsets['Name'][:-1], rrsets["ResourceRecords"][0]["Value"]])
    if doption == "table":
        print x

    elif doption == "html":
        print x.get_html_string()


def ec2Instances(awsConnConf, doption):
    # session client for ec2
    client = awsConnConf.session.client('ec2')
    # get the ec2 resource from the session
    ec2 = awsConnConf.session.resource('ec2')
    # all vpc information in the region
    allVpcs = client.describe_vpcs()
    print "EC2 Instances"
    # iterate over the vpc list
    for vpcs in allVpcs['Vpcs']:
        vpcid = vpcs['VpcId']
        print '\n'
        print '{0}'.format("\033[1m" + "Vpc Id" + "\033[0m")
        print '{0}'.format("------")
        print '{0}'.format(vpcs['VpcId'])
        print '\n'
        x = PrettyTable(["Instance Tag Name", "DNS Name", "Private IP Address", "Public IP Address", "AMI Id"])
        x.align["Instance Tag Name"] = "l"
        x.align["DNS Name"] = "l"
        x.align["Private IP Address"] = "l"
        x.align["Public IP Address"] = "l"
        x.align["AMI Id"] = "l"

        for item in client.describe_instances()['Reservations']:
            tagName = None
            dnsName = None
            pvtIpAddress = None
            pubIpAddress = None
            imageId = None

            if item['Instances'][0]['State']['Name'] == 'running':
                if item['Instances'][0].get('PublicDnsName'):
                    dnsName = item['Instances'][0]['PublicDnsName']

                if item['Instances'][0].get('PublicIpAddress'):
                    pubIpAddress = item['Instances'][0]['PublicIpAddress']

                if item['Instances'][0].get('PrivateIpAddress'):
                    pvtIpAddress = item['Instances'][0]['PrivateIpAddress']
            
                if item['Instances'][0].get('Tags'):
                    for tag in item['Instances'][0]['Tags']:
                        if tag['Key'] == 'Name':
                            tagName = tag['Value']
                if item['Instances'][0].get('ImageId'):
                    imageId = item['Instances'][0]['ImageId']

                x.add_row([tagName, dnsName, pvtIpAddress, pubIpAddress, imageId])

        if doption == "table":
            print x.get_string(sortby="Instance Tag Name")

        elif doption == "html":
            print x.get_html_string(sortby="Instance Tag Name")


def subnetInfo(awsConnConf, doption):
    #
    # session client for ec2
    client = awsConnConf.session.client('ec2')
    # get the ec2 resource from the session
    ec2 = awsConnConf.session.resource('ec2')
    # all vpc information in the region
    allVpcs = client.describe_vpcs()
    # iterate over the vpc list
    for vpcs in allVpcs['Vpcs']:
        vpcid = vpcs['VpcId']
        print '\n'
        print '{0}'.format("\033[1m" + "Vpc Id" + "\033[0m")
        print '{0}'.format("------")
        print '{0}'.format(vpcs['VpcId'])
        print '\n'
        subnet_name = None
        subnets = ec2.Vpc(vpcid).subnets.all()
        print "Subnet Information"
        x = PrettyTable(["Subnet Id", "CIDR Block", "Subnet - Friendly Name", "Avail. IP Count", "No. of Used IPs", "Availability Zone"])
        x.align["Subnet Id"] = "l"
        x.align["CIDR Block"] = "l"
        x.align["Subnet - Friendly Name"] = "l"
        x.align["Avail. IP Count"] = "l"
        x.align["No. of Used IPs"] = "l"
        x.align["Availability Zone"] = "l"

        for subnet in subnets:
            i = 0
            subnet_name = None
            for instance in subnet.instances.all():
                i += 1
        
            if subnet.tags: 
                for item in subnet.tags:
                    if item['Key'] == 'Name':
                        subnet_name = item['Value']
            x.add_row([subnet.subnet_id, 
                subnet.cidr_block, 
                subnet_name, 
                subnet.available_ip_address_count, 
                i,
                subnet.availability_zone])
        if doption == "table":
            print x.get_string(sortby="Subnet - Friendly Name")
        elif doption == "html":
            print x.get_html_string(sortby="Subnet - Friendly Name")


def sgInfo(awsConnConf, doption):
    #
    #
    # session client for ec2
    client = awsConnConf.session.client('ec2')
    # get the ec2 resource from the session
    ec2 = awsConnConf.session.resource('ec2')
    # all vpc information in the region
    allVpcs = client.describe_vpcs()
    # iterate over the vpc list
    for vpcs in allVpcs['Vpcs']:
        vpcid = vpcs['VpcId']
        print '\n'
        print '{0}'.format("\033[1m" + "Vpc Id" + "\033[0m")
        print '{0}'.format("------")
        print '{0}'.format(vpcs['VpcId'])
        print '\n'
        sentinel = object()
        secgroups = ec2.Vpc(vpcid).security_groups.all()
        print "Security Groups Information"
        x = PrettyTable(["Security Group Id", "Security Group Name", "ACLs - Source IP", "ACLs - ToPort"])
        x.align["Security Group Id"] = "l"
        x.align["Security Group Name"] = "l"
        x.align["ACLs - Source IP"] = "l"
        x.align["ACLs - ToPort"] = "l"
        size = 0
        i = 0
        for secgrp in secgroups:
            size += 1

        for secgrp in secgroups:
            ToPort = None
            IpRanges = list()
            x.add_row([secgrp.group_id, secgrp.group_name, "", ""])

            if len(secgrp.ip_permissions) != 0:
                for perm in secgrp.ip_permissions:
                    if perm.get('ToPort') != None:
                        ToPort = perm.get('ToPort')
                    if len(perm.get('IpRanges')) != 0:
                        IpRanges = perm.get('IpRanges')

                    if len(IpRanges) != 0:
                        for IpRange in IpRanges:
                            x.add_row(["", "", IpRange['CidrIp'], ToPort])
        
            if i < size - 1:
                x.add_row(["-------------------", 
                  "-------------------------------------------------", 
                  "------------------", 
                  "---------------"])
                i += 1
        if doption == "table":
            print x

        if doption == "html":
            print x.get_html_string()


def lisKeyPairs(client, doption):
    keypairs = client.describe_key_pairs()
    x = PrettyTable(["KeyName", "KeyFingerprint"])
    x.align["KeyName"] = "l"
    x.align["KeyFingerprint"] = "l"
    print("KeyPairs Available")
    for keypair in keypairs['KeyPairs']:
        x.add_row([keypair['KeyName'], keypair['KeyFingerprint']])

    if doption == "table":
        print x

    if doption == "html":
        print x.get_html_string()


def listAvailZones(client, doption):
    availZones = client.describe_availability_zones()
    x = PrettyTable(["RegionName", "ZoneName"])
    x.align["RegionName"] = "l"
    x.align["ZoneName"] = "l"
    print("Availability Zones")
    for zone in availZones['AvailabilityZones']:
        x.add_row([zone["RegionName"], zone["ZoneName"]])

    if doption == "table":
        print x

    if doption == "html":
        print x.get_html_string()


def listLoadBalancers(client, doption):
    print "Load Balancers"
    x = PrettyTable(["DNS Name", "Scheme"])
    x.align["DNS Name"] = "l"
    lbNames = []
    for item in client.describe_load_balancers()['LoadBalancerDescriptions']:
        x.add_row([item['DNSName'], item['Scheme']])

    if doption == "table":
        print x

    if doption == "html":
        print x.get_html_string()


def listAll(awsConnConf, doption):
    # session client for ec2
    client = awsConnConf.session.client('ec2')
    # get the ec2 resource from the session
    ec2 = awsConnConf.session.resource('ec2')
    # 'elb' client
    clientElb = awsConnConf.session.client('elb')
    # Route53 client
    clientR53 = awsConnConf.session.client('route53')
    # all subnets
    subnetInfo(awsConnConf, doption)
    # all sec groups
    sgInfo(awsConnConf, doption)
    # all ec2 instances
    ec2Instances(awsConnConf, doption)
    # list all keypairs
    lisKeyPairs(client, doption)
    # list availability zones
    print '\n'
    listAvailZones(client, doption)
    print '\n'
    listLoadBalancers(clientElb, doption)
    print '\n'
    getRoute53Records(clientR53, doption)


def parseCmdLineArgs():
    parser = ArgumentParser()

    parser.add_argument("-n", "--aws-account-id",
            action="store",
            required=True,
            dest="awsaccountid",
            help="AWS Account Number")

    parser.add_argument("-d", "--display-option",
            action="store",
            required=True,
            choices=["table", "html"],
            dest="doption",
            help="How do you want to display the results?")

    parser.add_argument("--list",
            action="store",
            required=True,
            choices=["all", "vpcs", "subnets"],
            dest="resources",
            help="How do you want to display the results?")

    args = vars(parser.parse_args())

    return args

if __name__=="__main__":
    args = parseCmdLineArgs()
    awsConnConf = AwsConnectionConfig(args["awsaccountid"])
    callfunc = {
        'all': 'listAll(awsConnConf, args["doption"])',
        'vpcs': 'listVpcs(awsConnConf, args["doption"])',
        'subnets': 'subnetInfo(awsConnConf, args["doption"])'
    }

    func = callfunc.get(args["resources"])
    eval(func)
