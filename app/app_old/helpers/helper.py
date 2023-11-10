import subprocess
import os
import pickle
from app.settings import SETTINGS_BD_PATH, DEFAULT_PICAM_SETTINGS


def get_ip():
    url = "icanhazip.com"
    res = subprocess.getoutput("/usr/bin/wget -O - -q {}".format(url))
    return "{}".format(res)


def _get_photos_from_path(abs_path, url_path=None, only_photo=False):
    lst = sorted(list(filter(lambda x: x.endswith('.jpg') and not 'thumbnail' in x, os.listdir(abs_path))))
    if url_path:
        return ["{}/{}".format(url_path, file) for file in lst][::-1]
    elif only_photo:
        return ["{}".format(file) for file in lst][::-1]
    return ["{}/{}".format(abs_path, file) for file in lst][::-1]


def _get_photos_thumb_from_path(abs_path, url_path=None):
    lst = sorted(list(filter(lambda x: x.endswith('.jpg') and 'thumbnail' in x, os.listdir(abs_path))))
    if url_path:
        return ["{}/{}".format(url_path, file) for file in lst][::-1]
    return ["{}/{}".format(abs_path, file) for file in lst][::-1]


def _del_all_files(path_list, format='.jpg', num=0):
    for path in path_list:
        files = os.listdir(path)
        all_format_files = list(filter(lambda x: x.endswith(format), files))
        photo_list = _get_photos_from_path(path)
        if num == 0:
            [os.remove('{}/{}'.format(path, f)) for f in all_format_files]
        else:
            if len(photo_list) > num:
                photo_thumb_list = _get_photos_thumb_from_path(path)
                os.remove(min(photo_list, key=os.path.getctime))
                os.remove(min(photo_thumb_list, key=os.path.getctime))


def _del_file(path, f):
    os.remove("{}/{}".format(path, f))
    files = os.listdir(path)
    file_thumb = list(filter(lambda x: x.endswith(f), files))
    os.remove("{}/{}".format(path, file_thumb[0]))


def get_config_cam():
    try:
        with open(SETTINGS_BD_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return DEFAULT_PICAM_SETTINGS


def set_config_cam(data):
    with open(SETTINGS_BD_PATH, 'wb') as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    get_ip()
