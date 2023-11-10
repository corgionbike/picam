from app import app
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FORMAT_DEBUG = '%(asctime)-15s: in %(filename)s %(message)s'
logging.basicConfig(filename='{}/camera.log'.format(BASE_DIR), format=FORMAT_DEBUG, level=logging.ERROR)

try:
    app.run(host='0.0.0.0', debug=True)
except Exception as e:
    logging.error(e)
