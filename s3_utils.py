import json
import boto3

BUCKET_NAME = 'reddit-runner'


def upload_json(data, name):
    """
    Will upload a given dictionary to a json file of a given name
    :param data: The dictionary to upload
    :param name: The name of the file
    """
    s3 = boto3.resource('s3')
    s3object = s3.Object(BUCKET_NAME, name)
    s3object.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))


def get_json(name):
    """
    Will get the json from a given s3 file
    :param name: The name of the file to retrieve
    :return: The dictionary representation of the json
    """
    s3 = boto3.resource('s3')
    content_object = s3.Object(BUCKET_NAME, name)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    return json.loads(file_content)
