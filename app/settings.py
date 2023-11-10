import os

#активация виртуального окружения
#source /home/pi/picam/picamenv/bin/activate


# абсолютный путь до файла settings.py, от него будут строиться все остальные адреса
BYTE_IN_GB = 1073741824
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAM_DISK_ABS_PATH = "/mnt/tmpfs"

PHOTO_PATH = "static/img/tmpfs"
PHOTO_ABS_PATH = '{}/{}'.format(BASE_DIR, PHOTO_PATH)

ARCHIVE_PATH = 'static/img/archive'
ARCHIVE_ABS_PATH = '{}/{}'.format(BASE_DIR, ARCHIVE_PATH)

ARCHIVE_THUMBNAIL_PATH = 'static/img/archive/thumbnail'
ARCHIVE_ABS_THUMBNAIL_PATH = '{}/{}'.format(BASE_DIR, ARCHIVE_THUMBNAIL_PATH)


VIDEO_PATH = 'static/video'.format(BASE_DIR)
VIDEO_ABS_PATH = '{}/{}'.format(BASE_DIR, VIDEO_PATH)

PHOTO_COUNT = 100
PHOTO_SHOW_COUNT = 10

RELOAD_INTERVAL = 3 * 1000 * 60  # minuts
COPY_TO_FTP_ARCHIVE_INTERVAL = 3 * 1000 * 60  # minuts

FTP_ARCHIVE_PATH = '/USB'
FTP_HOST = '192.168.1.1'
FTP_PORT = 21
FTP_USER = 'admin'
FTP_PASS = ''
FTP_SIZE = 5 * BYTE_IN_GB  #5GB

DEFAULT_PICAM_SETTINGS = {
    'rotation': 0,
    'saturation': 20,
    'sharpness': 10,
    'awb_mode': 'auto',
    'iso': 0,
    'monohrom': False,
    'auto_night': True,
    'annotate_text': False,
    'resolution': '3280x2464',
    'annotate_text_size': 48
}

SETTINGS_BD_PATH = "{}/static/config.pickle".format(BASE_DIR)


ROUTER_AUTH = {'user': 'admin', 'pass': 'Lion7422'}

