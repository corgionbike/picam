from time import sleep
from picamera import PiCamera
from picamera import PiCameraCircularIO
import picamera
import sys
sys.path.append('/home/pi/picam/app')
from settings import *
import subprocess
import shlex
from PIL import Image
from datetime import datetime, timedelta
import os
import ephem
from io import BytesIO
from fractions import Fraction
from datetime import timedelta


# import logging

# FORMAT_DEBUG = '%(asctime)-15s: in %(filename)s %(message)s'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename='{}/tl.log'.format(BASE_DIR), format=FORMAT_DEBUG, level=logging.ERROR)

VIDEO_RESOLUTION = (1920, 1080)
IMG_RESOLUTION_FHD = (1920, 1080)
IMG_RESOLUTION_QHD = (2560, 1440)
IMG_RESOLUTION_MAX = (3280, 2464)
THUMBNAIL_RESOLUTION = (640, 480)
SUNRISE_HOUR = 17
SUNSET_HOUR = 6
END_DATE = datetime(2018, 10, 11, hour=23, minute=0, second=0, microsecond=0)
DELAY = 2


class StatusSunCalc():

    def __init__(self, offset_minutes=20, caption='Vladimir', lat='56.143063', lon='40.410934', elevation=144.0):
        self._offset_minutes = offset_minutes
        sity = self._init_sity(caption, lat, lon, elevation)
        self._calc(sity)

    def _calc(self, sity):
        obs = ephem.Observer()
        obs.lat = sity.lat
        obs.long = sity.long
        sun = ephem._sun
        obs.date = datetime.now().date()
        rise_time = obs.next_rising(sun)
        set_time = obs.next_setting(sun)
        # print("sunrise:", ephem.localtime(rise_time).ctime())
        # print("sunset:", ephem.localtime(set_time).ctime())
        self.sunrise = ephem.localtime(rise_time)
        self.sunset = ephem.localtime(set_time) + timedelta(minutes=self._offset_minutes)

    def _init_sity(self, caption, lat, lon, elevation):
        o = ephem.Observer()
        o.name = caption
        o.lat, o.lon, o.elevation = (lat, lon, elevation)
        o.compute_pressure()
        return o


def get_exposure_mode(monohrom=False, auto_night=False):
    if monohrom:
        return ('night', (128, 128))
    if auto_night:
        now_hour = datetime.now().time()
        ss = StatusSunCalc()
        if now_hour < ss.sunrise.time() or now_hour > ss.sunset.time():
            return ('night', None)
    return ('auto', None)


def shoot(shots=1, sec=2, res=None, path=PHOTO_ABS_PATH, quality=99, config_cam=DEFAULT_PICAM_SETTINGS):
    with PiCamera(resolution=config_cam['resolution']) as camera:
        camera.rotation = config_cam['rotation']
        camera.saturation = config_cam['saturation']
        camera.sharpness = config_cam['sharpness']
        camera.awb_mode = config_cam['awb_mode']
        camera.iso = config_cam['iso']
        exposure_mode = get_exposure_mode(monohrom=config_cam['monohrom'], auto_night=config_cam['auto_night'])
        camera.exposure_mode = exposure_mode[0]
        camera.color_effects = exposure_mode[1]
        camera.annotate_foreground = picamera.Color('white')
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text_size = config_cam['annotate_text_size']
        sleep(DELAY)
        for i in range(shots):
            mem_foto = BytesIO()
            times = datetime.now()
            f_now = times.strftime('%Y%m%d%H%M%S')
            foto_full_path = '{}/photo_{}.{}'.format(path, f_now, 'jpg')
            if config_cam['annotate_text']:
                camera.annotate_text = times.strftime('%Y-%m-%d %H:%M:%S')
            camera.capture(mem_foto, format='jpeg', quality=quality)
            with Image.open(mem_foto) as im:
                im.save(foto_full_path)
                im.thumbnail(THUMBNAIL_RESOLUTION)
                im.save('{}/thumbnail_photo_{}.{}'.format(path, f_now, 'jpg'), 'JPEG')
            if shots > 1:
                sleep(sec)


def make_video(sec):
    try:
        with PiCamera(resolution=VIDEO_RESOLUTION, framerate=24) as camera:
            path = '{}/static/video'.format(BASE_DIR)
            video = '{}/last_video.h264'.format(path)
            video_mp4 = '{}/last_video.mp4'.format(path)
            camera.rotation = CameraConfig.rotation
            exposure_mode = get_exposure_mode()
            camera.exposure_mode = exposure_mode[0]
            camera.color_effects = exposure_mode[1]
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sleep(DELAY)
            camera.start_recording(video)
            camera.wait_recording(sec)
            camera.stop_recording()
            command = shlex.split("MP4Box -add {f} {m}".format(f=video, m=video_mp4))
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            return path
    except Exception as e:
        return False


def circular_video(sec=15, framerate=10):
    with PiCamera(resolution=VIDEO_RESOLUTION) as camera:
        camera.framerate = framerate
        camera.frame = None
        stream = PiCameraCircularIO(camera, seconds=sec)
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(sec)
                dt = datetime.now().strftime('%Y%m%d%H%M%S')
                video = '{}/video_{}.h264'.format(VIDEO_ABS_PATH, dt)
                stream.copy_to(video)
        finally:
            camera.stop_recording()


if __name__ == "__main__":
    circular_video()
