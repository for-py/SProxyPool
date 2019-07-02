import logging
import colorlog
import os
import sys

cur_path = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch_fmt = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s -%(levelname)s -%(pathname)s -%(funcName)s -%(lineno)s -%(message)s',
    log_colors={'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red'})
fh_fmt = logging.Formatter('%(asctime)s, %(message)s')

fh = logging.FileHandler(filename=os.path.join(cur_path, 'error.txt'))
fh.setLevel(logging.ERROR)
fh.setFormatter(fh_fmt)

ch = colorlog.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(ch_fmt)

logger.addHandler(fh)
logger.addHandler(ch)

