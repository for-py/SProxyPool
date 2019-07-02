import redis
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from settings import INITIAL_SCORE, PROXY_ORIGINAL, PROXY_VALIDATED, \
    VALIDATED_SCORE, DISCARD_SCORE
import re
from utility import Utility
from tools.logger import logger


class RedisClient(Utility):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.pattern = re.compile(
            r'^http[s]?://((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}:\d{0,5}$')

    def add(self, proxy, name=PROXY_ORIGINAL, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param score: 默认分值
        :param name:键名
        :param proxy: 代理
        :return: 添加结果
        """
        ip_port = proxy.split('-')[1]
        match = self.pattern.match(ip_port)
        if match:
            if not self.db.zscore(name, proxy):
                return self.db.zadd(name, {proxy: score})
            else:
                logger.info('proxy %s already exists' % proxy)
                if int(self.db.zscore(name, proxy)) == 100:
                    return self.db.zadd(name, {proxy: INITIAL_SCORE})
        else:
            logger.warning('illegal proxy: %s' % proxy)

    def adjust_score(self, proxy, decr_by, key=PROXY_ORIGINAL):
        """
        加分或减分操作
        :param key: redis key name
        :param decr_by: 改变的分数
        :param proxy: 代理的值
        :return: 修改后的代理分数
        """
        if decr_by > 0:
            if key == PROXY_ORIGINAL:
                self.db.zadd(PROXY_VALIDATED, {proxy: VALIDATED_SCORE})
            self.db.zadd(key, {proxy: VALIDATED_SCORE})
            logger.info('valid proxy: %s' % proxy)
        else:
            score = int(self.db.zincrby(key, decr_by, proxy))
            if score <= DISCARD_SCORE:
                logger.info('abandon proxy: %s' % proxy)
                if key == PROXY_VALIDATED:
                    self.db.zrem(PROXY_VALIDATED, proxy)
            elif DISCARD_SCORE < score <= INITIAL_SCORE:
                logger.info('waiting for further check %s' % proxy)

    def valid_proxy(self, proxy, name=PROXY_ORIGINAL):
        self.db.zadd(name, {proxy: 100})
        self.db.zrem(PROXY_ORIGINAL, proxy)
        if not self.db.zscore(PROXY_VALIDATED, proxy):
            self.db.zadd(PROXY_VALIDATED, {proxy: 100})

    def count(self, min_score, max_score, name=PROXY_ORIGINAL):
        """
        获取数量
        :type min_score: 最低分数
        :type max_score: 最高分值
        :type name: 指定redis key
        :return: 数量
        """
        min_ = min_score
        max_ = max_score
        name_ = name
        return self.db.zcount(name_, min_, max_)

    def get_proxy_by_score(self, min_score, max_score, fetch_num, key=PROXY_ORIGINAL):
        """
        :param key: redis key name
        :param fetch_num: 一次取出的proxy的数量
        :param min_score:
        :param max_score:
        :return:
        """
        name = key
        return self.db.zrevrangebyscore(name, max_score, min_score, start=0, num=fetch_num)


if __name__ == '__main__':
    pass
