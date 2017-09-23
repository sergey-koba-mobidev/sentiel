# Sentiel
A Raspberry Pi Python based scypt, which takes picture and uploads it to S3 bucket.
Can be run by crontab on regular basis.

## Install
- `pip install boto3`
- `pip install pyyaml`
- `sudo apt-get install libjpeg-dev`
- `pip install Pillow`
- create `config.yml`

```yml
region_name:  'nyc3'
endpoint_url: 'https://nyc3.digitaloceanspaces.com'
aws_access_key_id: '...'
aws_secret_access_key: '...'
s3_folder: 'sentiel'
bucket: 'my-bucket'
sentiel_name: 'aragorn'
expire_days: 7
```

## Run
- `python sentiel.py`

## Pictures
All pictures are stored in `/home/pi/sentiel` folder