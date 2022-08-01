"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

config = pulumi.Config()
name = config.require('name')

if (name=="backup"):
# Create an AWS resource (S3 Bucket)
    bucket = s3.Bucket('backup-bucket')
# Export the name of the bucket
    pulumi.export('bucket_name', bucket.id)
