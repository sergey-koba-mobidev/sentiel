import os, errno, picamera, datetime, boto3, yaml, io, time, shutil
from botocore.client import Config
from PIL import Image

def main():
    # Read config YAML file
    with open("config.yml", 'r') as stream:
        config_loaded = yaml.load(stream)

    now = datetime.datetime.now()
    ROOT_DIR = config_loaded['save_dir'] + "/pictures/" + now.strftime("%Y-%m-%d") + "/"

    # Create root Dir for pictures
    try:
        os.makedirs(ROOT_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        os.makedirs(ROOT_DIR + "thumbnails")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Take a picture
    camera = picamera.PiCamera()
    camera.vflip = config_loaded['vflip']
    camera.hflip = config_loaded['hflip']
    camera.brightness = config_loaded['brightness']
    camera.contrast = config_loaded['contrast']
    file_name = now.strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
    camera.capture(ROOT_DIR + file_name)
    print "Made a picture " + ROOT_DIR + file_name
    # Create thumbnail
    size = 128, 128
    im = Image.open(ROOT_DIR + file_name)
    im.thumbnail(size)
    im.save(ROOT_DIR + 'thumbnails/' + file_name, "JPEG")
    print "Saved thumbnail " + ROOT_DIR + 'thumnails/' + file_name

    # Upload picture to S3
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=config_loaded['region_name'],
                            endpoint_url=config_loaded['endpoint_url'],
                            aws_access_key_id=config_loaded['aws_access_key_id'],
                            aws_secret_access_key=config_loaded['aws_secret_access_key'])

    upload_filename = 'sentinels/' + config_loaded['sentiel_name'] + '/pictures/' + now.strftime("%Y-%m-%d") + '/' + file_name
    upload_th_filename = 'sentinels/' + config_loaded['sentiel_name'] + '/pictures/' + now.strftime("%Y-%m-%d") + '/thumbnails/' + file_name
    client.upload_file(ROOT_DIR + file_name,
                       config_loaded['bucket'],
                       upload_filename,
                       ExtraArgs={'ACL': 'public-read'})
    print "Uploaded " + upload_filename

    client.upload_file(ROOT_DIR + 'thumbnails/' + file_name,
                       config_loaded['bucket'],
                       upload_th_filename,
                       ExtraArgs={'ACL': 'public-read'})
    print "Uploaded " + upload_th_filename

    # Cleanup local files
    for r,d,f in os.walk(config_loaded['save_dir'] + "/pictures/"):
        for dir in d:
            if dir != 'thumbnails':
                date = datetime.datetime.strptime(dir.replace(".jpg",""), "%Y-%m-%d")
                if (now - date).days > config_loaded['expire_days']:
                    try:
                        print "removing ",os.path.join(r,dir)
                        shutil.rmtree(os.path.join(r,dir))
                    except Exception,e:
                        print e
                        pass
                    else: 
                        print "Removed " + os.path.join(r,dir)

    # Cleanup S3
    result = client.list_objects(Bucket=config_loaded['bucket'], Prefix='sentinels/' + config_loaded['sentiel_name'] + '/pictures/', Delimiter='/')
    for o in result.get('CommonPrefixes'):
        dir = o.get('Prefix')
        date = datetime.datetime.strptime(dir.replace('sentinels/' + config_loaded['sentiel_name'] + '/pictures/',""), "%Y-%m-%d/")
        if (now - date).days > config_loaded['expire_days']:
            res = client.list_objects(Bucket=config_loaded['bucket'], Prefix=dir)    
            for obj in res.get('Contents'):
                print("Deleting from S3 " + obj.get('Key'))
                client.delete_object(Bucket=config_loaded['bucket'], Key=obj.get('Key'))

try:
    main()
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    if e.errno == errno.EEXIST:
        print "No space removing local pictures"
        with open("config.yml", 'r') as stream:
            config_loaded = yaml.load(stream)
        shutil.rmtree(os.path.join(r,config_loaded['save_dir'] + "/pictures/"))
        
    
