# Sentiel
A Raspberry Pi Python based scypt, which takes picture and uploads it to S3 bucket.
Can be run by crontab on regular basis.

## Install
- `pip install boto3`
- `pip install pyyaml`
- create `config.yml`

## Run
- `python sentiel.py`

## Pictures
All pictures are stored in `/home/pi/sentiel` folder