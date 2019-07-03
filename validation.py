from settings import TEST_URL, CONCURRENCY_TASK_LIMIT, INITIAL_SCORE, VALIDATE_TIME, DISCARD_SCORE, PROXY_ORIGINAL
import aiohttp
from settings import ANON_CHECK_URL
from db import RedisClient
import asyncio
from tools.randomua import get_random_ua
from aiohttp.client_exceptions import ClientConnectionError, ClientHttpProxyError, ClientProxyConnectionError
from asyncio import TimeoutError, CancelledError
import requests
from utility import Utility
from tools.logger import logger


class IpValidation(Utility):

    def __init__(self):
        self.redis = RedisClient()
        self.real_ip = ''
        # 每次验证不成功，减去的分值
        self.minus_every_time = (INITIAL_SCORE - DISCARD_SCORE) // VALIDATE_TIME
        self.key = PROXY_ORIGINAL
        self.anon_check_url = 'http://httpbin.org/ip'

    @staticmethod
    async def is_proxy_valid(proxy, url=TEST_URL):
        url = url
        ua = get_random_ua()
        headers = {'User-Agent': ua}
        try:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(headers=headers, connector=conn) as session:
                async with session.get(url, proxy=proxy, ssl=False) as resp:
                    code = resp.status
                    if 200 <= code < 300:
                        logger.info('%s is valid' % proxy)
                        return True
                    else:
                        logger.info('%s is invalid, code: %s' % (proxy, code))
                        return False
        except (ClientConnectionError, ClientHttpProxyError,
                TimeoutError, CancelledError, ClientProxyConnectionError, Exception) as e:
            logger.warning(e)
            return False

    async def is_high_anon(self, proxy):
        url = ANON_CHECK_URL
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy, ssl=False, timeout=15) as resp:
                    code = resp.status
                    if 200 <= code < 300:
                        x_forwarded_for_json = await resp.json()
                        if self.anon_check_url == ANON_CHECK_URL:
                            x_forwarded_for = x_forwarded_for_json['origin']
                        else:
                            # 根据接口自己定义
                            x_forwarded_for = x_forwarded_for_json['X-Forwarded-For']
                        if self.real_ip in x_forwarded_for:
                            return False
                        return True
                    return False
        except (ClientConnectionError, ClientHttpProxyError,
                TimeoutError, CancelledError, ClientProxyConnectionError, Exception) as e:
            logger.warning('proxy: %s, %s' % (proxy, e))
            return False

    async def test_proxy(self, proxy):
        try:
            if len(proxy.split('-')[1]) > 1:
                if not await self.is_high_anon(proxy.split('-')[1].replace('https://', 'http://')):
                    self.redis.adjust_score(proxy, -self.minus_every_time, key=self.key)
                else:
                    self.redis.adjust_score(proxy, +1, key=self.key)
        except CancelledError as e:
            logger.warning('proxy: %s, %s' % (proxy, e))

    def get_real_ip(self):
        resp = requests.get(ANON_CHECK_URL)
        if self.anon_check_url == ANON_CHECK_URL:
            self.real_ip = resp.json()['origin'].split(',')[0]
        else:
            self.real_ip = resp.json()['X-Real-Ip']

    def run_validation(self, key=None):
        if key:
            self.key = key
        logger.info('start checking...')
        start, end = DISCARD_SCORE+1, INITIAL_SCORE
        while True:
            proxy_unvalidated = self.redis.count(start, end, name=self.key)
            if proxy_unvalidated:
                logger.info('checking...')
                if proxy_unvalidated <= CONCURRENCY_TASK_LIMIT:
                    self.get_real_ip()
                    proxy_list = self.redis.get_proxy_by_score(start, end, proxy_unvalidated, key=self.key)
                    # loop = asyncio.get_event_loop()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    tasks = [self.test_proxy(proxy) for proxy in proxy_list]
                    loop.run_until_complete(asyncio.wait(tasks))
                else:
                    fetch_times = proxy_unvalidated // CONCURRENCY_TASK_LIMIT
                    left_nums = proxy_unvalidated // CONCURRENCY_TASK_LIMIT
                    for i in range(fetch_times):
                        self.get_real_ip()
                        proxy_list = self.redis.get_proxy_by_score(start, end, CONCURRENCY_TASK_LIMIT, key=self.key)
                        # loop = asyncio.get_event_loop()
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        tasks = [self.test_proxy(proxy) for proxy in proxy_list]
                        loop.run_until_complete(asyncio.wait(tasks))
                    proxy_list = self.redis.get_proxy_by_score(start, end, left_nums, key=self.key)
                    # loop = asyncio.get_event_loop()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    tasks = [self.test_proxy(proxy) for proxy in proxy_list]
                    loop.run_until_complete(asyncio.wait(tasks))
            import settings
            if not proxy_unvalidated and not settings.SPIDER_RUNNING:
                settings.SPIDER_RUNNING = True
                self.key = PROXY_ORIGINAL
                logger.info('scrawl finished，all proxies check finished')
                break


if __name__ == '__main__':
    valid = IpValidation()
    valid.run_validation()
