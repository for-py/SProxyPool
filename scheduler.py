from downloader import DownLoader
from validation import IpValidation
from multiprocessing import Pool
import time
from db import RedisClient
from settings import VALIDATED_SCORE
from tools.logger import logger


class Scheduler(object):
    def __init__(self):
        self.downloader = DownLoader()
        self.valid = IpValidation()
        self.redis = RedisClient()

    def run_spider(self):
        start = time.time()
        p = Pool(4)
        # 开启爬虫
        p.apply_async(self.downloader.start_crawl())
        # 开启代理检测
        p.apply_async(self.valid.run_validation())

        p.close()
        p.join()
        end = time.time()
        logger.info('proxy crawl and validation are done!')
        valid_proxy_num = self.redis.count(VALIDATED_SCORE, VALIDATED_SCORE)
        logger.info('time used: %s, valid proxies are: %s' % ((end-start), valid_proxy_num))
