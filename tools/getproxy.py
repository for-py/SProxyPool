from db import RedisClient
from settings import PROXY_VALIDATED, PROXY_FOR_USE
from tools.logger import logger


class GetProxy:
    def __init__(self):
        self.redis = RedisClient()

    def clear_old_key(self):
        min_, max_ = '-inf', '+inf'
        length = self.redis.count(min_, max_, name=PROXY_FOR_USE)
        if length > 0:
            self.redis.db.zremrangebyrank(PROXY_FOR_USE, 0, -1)

    def init_redis_key(self):
        self.clear_old_key()
        min_, max_ = '-inf', '+inf'
        length = self.redis.count(min_, max_)
        if length > 0:
            self.redis.db.zunionstore(PROXY_FOR_USE, [PROXY_VALIDATED])

    def get_proxy(self):
        min_, max_ = '-inf', '+inf'
        length = self.redis.count(min_, max_, name=PROXY_FOR_USE)
        if length > 0:
            proxy = self.redis.get_proxy_by_score(min_, max_, 1, key=PROXY_FOR_USE)[0].split('-')[1]
            return proxy
        else:
            raise Exception('no proxy to use')


if __name__ == '__main__':
    gt = GetProxy()
    logger.info(gt.get_proxy())