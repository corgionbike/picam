import datetime as dt
import re
import shutil

import psutil
from flask import url_for, render_template, redirect, request, jsonify, flash

from app import app
from app.api.camera import shoot, make_video as mv, StatusSunCalc
from app.api.servo import get_calibr, set_calibr
from app.api.servo import set_servo as setServo
from app.forms import SettingsForm
from app.helpers.helper import get_ip as ip, _get_photos_from_path, _get_photos_thumb_from_path, _del_all_files, \
    _del_file, get_config_cam, set_config_cam
from app.settings import *


@app.template_filter('getdatetime')
def getmodtime_filter(file):
    try:
        regex = r"_(.*)\."
        result = re.findall(regex, file)
        date = dt.datetime.strptime(result[0], '%Y%m%d%H%M%S')
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        pass


@app.context_processor
def settings():
    return dict(RELOAD_INTERVAL=RELOAD_INTERVAL)


@app.context_processor
def status_sun_processor():
    ss = StatusSunCalc(offset_minutes=0)
    sun = ss.sunrise
    moon = ss.sunset
    return dict(moon=moon.strftime("%H:%M"), sun=sun.strftime("%H:%M"))


@app.context_processor
def calibr_processor():
    data = get_calibr()
    return dict(x=data['x'], y=data['y'])


@app.context_processor
def get_ip():
    return dict(my_ip=ip())


@app.route("/")
def index():
    photo_list = _get_photos_from_path(PHOTO_ABS_PATH, url_path=PHOTO_PATH)
    photo_list_thumbnail = _get_photos_thumb_from_path(PHOTO_ABS_PATH, url_path=PHOTO_PATH)
    time = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('index', _external=True)
    return render_template('index.html', photo_list=photo_list[:PHOTO_SHOW_COUNT],
                           photo_list_thumbnail=photo_list_thumbnail[:PHOTO_SHOW_COUNT],
                           time=time)


@app.route("/reload")
def reload_photo_list():
    photo_list = _get_photos_from_path(PHOTO_ABS_PATH, url_path=PHOTO_PATH)
    photo_list_thumbnail = _get_photos_thumb_from_path(PHOTO_ABS_PATH, url_path=PHOTO_PATH)
    return jsonify(
        {'photo_list': photo_list[:PHOTO_SHOW_COUNT], 'photo_list_thumbnail': photo_list_thumbnail[:PHOTO_SHOW_COUNT]})


@app.route('/copy_to_archive')
def copy_to_archive():
    s = request.args.get('s', 1, type=int)
    photo_array = _get_photos_from_path(PHOTO_ABS_PATH)[:s]
    photo_array_thumb = _get_photos_thumb_from_path(PHOTO_ABS_PATH)[:s]
    try:
        for f in (photo_array + photo_array_thumb):
            shutil.copy(f, ARCHIVE_ABS_PATH)
    except Exception as e:
        return jsonify({'Error': e})
    return jsonify({'response': "Ok", 'count': s})


@app.route("/shoot")
@app.route("/shoot/<int:shots>")
def make_shoot(shots=1):
    _del_all_files([PHOTO_ABS_PATH], num=PHOTO_COUNT)
    s = request.args.get('s', None, type=int)
    t = request.args.get('t', None, type=int)
    try:
        if s and t:
            shoot(shots=s, sec=t, config_cam=get_config_cam())
        else:
            shoot(shots, config_cam=get_config_cam())
            return jsonify({'shoot': 'Ok'})
    except Exception as error:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(error).__name__, error.args)
        return render_template('error.html', error=message)
    flash('Кадр успешно сделан...')
    return redirect(url_for('index'))


@app.route("/archive")
def archive():
    photo_archive = _get_photos_from_path(ARCHIVE_ABS_PATH, url_path=ARCHIVE_PATH)
    photo_archive_thumb = _get_photos_thumb_from_path(ARCHIVE_ABS_PATH, url_path=ARCHIVE_PATH)
    photo_archive_abs = _get_photos_from_path(ARCHIVE_ABS_PATH, only_photo=True)
    return render_template('archive.html', photo_archive=photo_archive,
                           photo_archive_thumb=photo_archive_thumb,
                           photo_archive_abs=photo_archive_abs,
                           time=dt.datetime.now())


@app.route("/settings", methods=('GET', 'POST'))
def settings():
    form = SettingsForm()
    if request.method == 'GET':
        config = get_config_cam()
        form.rotation.data = config.get('rotation')
        form.saturation.data = config.get('saturation')
        form.sharpness.data = config.get('sharpness')
        form.awb_mode.data = config.get('awb_mode')
        form.iso.data = config.get('iso')
        form.monohrom.data = config.get('monohrom')
        form.auto_night.data = config.get('auto_night')
        form.annotate_text.data = config.get('annotate_text')
        form.resolution.data = config.get('resolution')
        form.annotate_text_size.data = config.get('annotate_text_size')
    else:
        if form.validate_on_submit():
            new_config = {
                'rotation': form.rotation.data,
                'saturation': form.saturation.data,
                'sharpness': form.sharpness.data,
                'awb_mode': form.awb_mode.data,
                'iso': form.iso.data,
                'monohrom': form.monohrom.data,
                'auto_night': form.auto_night.data,
                'annotate_text': form.annotate_text.data,
                'resolution': form.resolution.data,
                'annotate_text_size': form.annotate_text_size.data
            }
            set_config_cam(new_config)
            flash('Настройки успешно сохранены...')
            return redirect(url_for('settings'))
    return render_template('settings.html', form=form)


@app.route("/settings/reset")
def settings_reset():
    set_config_cam(DEFAULT_PICAM_SETTINGS)
    flash('Настройки успешно сброшены...')
    return redirect(url_for('settings'))


@app.route("/archive/shoot")
def make_shoot2archive():
    try:
        shoot(path=ARCHIVE_ABS_PATH, config_cam=get_config_cam())
    except Exception as error:
        return render_template('error.html', error=error)
    flash('Кадр успешно сохранен в архив...')
    return redirect(url_for('archive'))


@app.route("/archive/clear")
def clear_archive():
    _del_all_files([ARCHIVE_ABS_PATH])
    flash('Архив успешно очищен...')
    return redirect(url_for('archive'))


@app.route("/archive/del/<string:shot>")
def del_photo_in_archive(shot=None):
    if shot:
        _del_file(ARCHIVE_ABS_PATH, shot)
    return jsonify({'response': "Ok"})


@app.route("/video")
def video():
    path = '{}/static/video'.format(BASE_DIR)
    files = os.listdir(path)
    video_archive = list(filter(lambda x: x.endswith('.mp4'), files))
    time = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    return render_template('video.html', video_archive=video_archive, time=time)


@app.route("/video/shoot/")
@app.route("/video/shoot/<int:sec>")
def make_video(sec=10):
    _del_all_files(['{}/static/video'.format(BASE_DIR)], format='.mp4')
    if not mv(sec):
        return render_template('error.html')
    return redirect(url_for('video'))


@app.route('/set_servo')
def set_servo():
    d = get_calibr()
    x = request.args.get('x', 0, type=int)
    y = request.args.get('y', 0, type=int)
    setServo(x + d['x'], y + d['y'])
    print(d)
    return jsonify({'x': x - d['x'], 'y': y - d['y']})


@app.route('/set_calibration')
def set_calibration():
    x = request.args.get('x', 0, type=int)
    y = request.args.get('y', 0, type=int)
    data = {'x': x, 'y': y}
    set_calibr(data)
    return jsonify(data)


@app.route('/sys_info')
def get_sys_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0].current
    data = {'cpu': "%.2d" % cpu, 'ram': "%.2d" % ram, 'cpu_temp': "%.2d" % cpu_temp}
    return jsonify(data)
