if 'vflip:' not in open('config.yml').read():
    with open("config.yml", "a") as config_file:
        config_file.write("\nvflip: true")
        print("[INFO] modified config.yml: added vflip key")

if 'hflip:' not in open('config.yml').read():
    with open("config.yml", "a") as config_file:
        config_file.write("\nhflip: true")
        print("[INFO] modified config.yml: added hflip key")
