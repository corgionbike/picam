import time
import pickle
from app.settings import BASE_DIR

# Servo Channel 1 =&amp;gt; GPIO 17    80 до 249
servoXChannel = "P1-12"
servoYChannel = "P1-7"

CALIBRATION = {
    'x': 0,
    'y': 0,
    'zoom': (0.0, 0.0, 1.0, 1.0)
}

BD_PATH = "{}/static/calibr.pickle".format(BASE_DIR)


def get_calibr():
    try:
        with open(BD_PATH, 'rb') as f:
            data = pickle.load(f)
            return data
    except Exception:
        return CALIBRATION


def set_calibr(data):
    with open(BD_PATH, 'wb') as f:
        pickle.dump(data, f)


def set_servo(x, y):
    servoStr = bytes("{}={}\n{}={}\n".format(servoXChannel, x, servoYChannel, y), 'utf-8')
    with open("/dev/servoblaster", "wb") as f:
        f.write(servoStr)


if __name__ == '__main__':
    pass