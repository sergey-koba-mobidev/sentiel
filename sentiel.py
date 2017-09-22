# TODO: update Readme, upload to github, create directories for pictures locally
import os, errno, picamera, datetime, boto3, yaml, io
from botocore.client import Config

ROOT_DIR = "/home/pi/sentiel/pictures/"

# Create root Dir for pictures
try:
    os.makedirs(ROOT_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Take a picture
camera = picamera.PiCamera()
camera.vflip = True
now = datetime.datetime.now()
file_name = now.strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
camera.capture(ROOT_DIR + file_name)

# Read config YAML file
with open("config.yml", 'r') as stream:
    config_loaded = yaml.load(stream)

# Upload picture to S3
session = boto3.session.Session()
client = session.client('s3',
                        region_name=config_loaded['region_name'],
                        endpoint_url=config_loaded['endpoint_url'],
                        aws_access_key_id=config_loaded['aws_access_key_id'],
                        aws_secret_access_key=config_loaded['aws_secret_access_key'])

upload_filename = 'sentiels/' + config_loaded['sentiel_name'] + '/pictures/' + now.strftime("%Y-%m-%d") + '/' + file_name
client.upload_file(ROOT_DIR + file_name,
                   config_loaded['bucket'],
                   upload_filename,
                   ExtraArgs={'ACL': 'public-read'})

# Cleanup local files

# Cleanup S3
