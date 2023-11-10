from time import sleep
from picamera import PiCamera
import os
from datetime import datetime, timedelta
import logging

FORMAT_DEBUG = '%(asctime)-15s: in %(filename)s %(message)s'
YA_DIR = "/mnt/yandex.disk/timelapse"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename='{}/tl.log'.format(BASE_DIR), format=FORMAT_DEBUG, level=logging.ERROR)

resolution = (1920, 1080)
SUNRISE_HOUR = 17
SUNSET_HOUR = 6
END_DATE = datetime(2018, 10, 11, hour=23, minute=0, second=0, microsecond=0)


def get_exposure_mode():
    now_hour = datetime.now().hour
    if now_hour >= SUNRISE_HOUR or now_hour < SUNSET_HOUR:
        return ('night', (128, 128))
    return ('auto', None)


def timelapse(minute=1):
    YA_DIR = "/mnt/yandex.disk/timelapse"
    try:
        with PiCamera(resolution=resolution) as camera:
            camera.rotation = 180
            camera.awb_mode = 'cloudy'
            camera.exposure_mode = get_exposure_mode()[0]
            camera.color_effects = get_exposure_mode()[1]
            print('Start timelapse mode...')
            sleep(2)
            i = 0
            while END_DATE < datetime.now():
                if not os.path.exists(YA_DIR):
                    YA_DIR = "/tmp"
                path = '{path}/img_{counter}.jpg'.format(path=YA_DIR, counter=i)
                camera.capture(path, quality=90)
                print(path)
                sleep(minute * 60)
                i += 1
    except KeyboardInterrupt:
        print('Mode stop manual')
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    timelapse()
