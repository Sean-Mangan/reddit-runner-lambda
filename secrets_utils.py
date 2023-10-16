import json
import os

import boto3

from botocore.exceptions import ClientError


def set_secrets():
    secret_name = "reddit-runner/secrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(e)
        raise

    # Decrypts secret using the associated KMS key.
    secrets = json.loads(get_secret_value_response["SecretString"])
    for key, value in secrets.items():
        os.environ[key] = value