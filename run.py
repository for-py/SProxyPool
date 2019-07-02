from scheduler import Scheduler
from tools.logger import logger


def run():
    sch = Scheduler()
    try:
        sch.run_spider()
    except Exception:
        logger.error('ERROR', exc_info=True)


if __name__ == '__main__':
    run()