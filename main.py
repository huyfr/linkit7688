import logging
import os
from logging.handlers import RotatingFileHandler

try:
    if not os.path.isfile('./config/default_data.py'):
        os.system('cp ./config/factory_data.py ./config/default_data.py')
except Exception as e:
    print 'Error ' + str(e)

from operate import main_thread


def main():
    from config import shared_attributes, default_data
    temp_level = shared_attributes.get('mccLogLevel', default_data.mccLogLevel)
    from control.utils import validate_log_level
    level = validate_log_level(temp_level)
    root = logging.getLogger('App')
    root.setLevel(level)
    size_bytes = 1500000  # bytes
    handler = RotatingFileHandler('app.log', mode='a', maxBytes=size_bytes, backupCount=1, encoding=None, delay=False)
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    handler.setLevel(logging.DEBUG)
    # run
    main_thread.call()


if __name__ == "__main__":
    main()
