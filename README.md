# Sentinel
A Raspberry Pi Python based scypt, which takes picture and uploads it to S3 bucket.
Can be run by crontab on regular basis.

## Install
- run `wget -O - https://raw.githubusercontent.com/sergey-koba-mobidev/sentinel/master/install.sh | sh`
- modify `config.yml`

```yml
region_name:  'nyc3'
endpoint_url: 'https://nyc3.digitaloceanspaces.com'
aws_access_key_id: '...'
aws_secret_access_key: '...'
bucket: 'my-bucket'
sentiel_name: 'aragorn'
expire_days: 7
save_dir: '/home/pi/sentinel'
brightness: 50
contrast: 50
vflip: false
hflip: false
```

## Run
- `./sentinel.sh`

## Add to crontab
- `crontab -e`
- add line `* * * * * cd /home/pi/Projects/sentinel && ./sentinel.sh >> log.txt`

## Pictures
All pictures are stored in `save_dir` folder
