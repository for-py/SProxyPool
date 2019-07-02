from db import RedisClient
from run import run
from validation import IpValidation
from settings import VALIDATED_SCORE, VALIDATED_PROXY_NUM, INITIAL_SCORE, DISCARD_SCORE, PROXY_VALIDATED
import settings
from tools.logger import logger
from utility import Utility


class ProxyCheck(Utility):
    def __init__(self):
        self.redis = RedisClient()
        self.valid = IpValidation()

    def check_num(self):
        valid_num = self.redis.count(VALIDATED_SCORE, VALIDATED_SCORE, name=PROXY_VALIDATED)
        if valid_num < VALIDATED_PROXY_NUM:
            run()

    def init_score(self):
        start, end = DISCARD_SCORE, '+inf'
        length = self.redis.count(start, end, name=PROXY_VALIDATED)
        while length > 0:
            result = self.redis.get_proxy_by_score(start, end, 1000)
            for ip in result:
                self.redis.db.zadd(PROXY_VALIDATED, {ip: INITIAL_SCORE})
            start += 1000
            length = self.redis.count(start, end)
        logger.info('initiation finished')

    def check_valid(self):
        settings.SPIDER_RUNNING = False
        self.init_score()
        self.valid.run_validation(key=PROXY_VALIDATED)
        self.check_num()


if __name__ == '__main__':
    pc = ProxyCheck()
    pc.check_valid()