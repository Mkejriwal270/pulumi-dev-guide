"""An AWS Python Pulumi program for conditional execution"""
import os
import pulumi
import pulumi_aws as aws
import requests
import time
import logging

url = os.getenv("MOCKAPI_URL")

config = pulumi.Config()
name = config.require('name')
tasks = config.get('tasks')
tasks = [1,2,3]

if (name=="backup"):
# Create an AWS resource (S3 Bucket)
    bucket = aws.s3.Bucket('backup-bucket')
# Export the name of the bucket
    pulumi.export('bucket_name', bucket.id)

ubuntu = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])

web = {}

if(url):
    for task_id in tasks:
        completed = False
        while (not completed):
            req = requests.get(f"{url}/{task_id}")
            #pulumi.log.debug(req.json())
            completed = req.json()["completed"]
            if (completed):
                break
            time.sleep(5)
        web[task_id] = aws.ec2.Instance(f"web-{task_id}",
            ami=ubuntu.id,
            instance_type="t2.micro",
            tags={
                "Task": f"Pulumi-{task_id}",
            })
        