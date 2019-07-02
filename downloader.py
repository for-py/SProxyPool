import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientConnectionError, ClientHttpProxyError, ClientProxyConnectionError
from asyncio import CancelledError
import random
import time
from settings import GFW_PROXY, VALIDATED_SCORE, VALIDATED_PROXY_NUM
import settings
from rules import rules
from spider import ProxySpider
from db import RedisClient
from utility import Utility
from tools.logger import logger
from tools.crackAntiCrawl import CrackAntiCrawl


class DownLoader(Utility):
    def __init__(self):
        self.rules = rules
        self.spider = ProxySpider()
        self.redis = RedisClient()
        self.crack_anti_crawl = CrackAntiCrawl()

    def start_crawl(self):
        for start_urls in self.rules:
            urls = start_urls['resources']
            gfw = start_urls['GFW']
            name = start_urls['name']
            page_type = start_urls['type']
            referer = start_urls['referer']
            host = start_urls['host']
            anti_crawl = start_urls['AntiCrawl']

            cookies = None
            if anti_crawl:
                cookies = eval('crack()', {'crack': eval('self.crack_anti_crawl.crack_{}'.format(name))})

            ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'
            headers = {'User-Agent': ua, 'Referer': referer, 'Host': host}
            # loop = asyncio.get_event_loop()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [self.proxy_downlaod(url, gfw, page_type, name, headers, cookies) for url in urls]
            loop.run_until_complete(asyncio.wait(tasks))
            # 检测有效proxy数量，达到指定数量，停止爬取
            validated_proxy_num = self.redis.count(VALIDATED_SCORE, VALIDATED_SCORE)
            if validated_proxy_num >= VALIDATED_PROXY_NUM:
                break
        settings.SPIDER_RUNNING = False
        logger.info('scrawl finished')

    async def proxy_downlaod(self, url, gfw, page_type, name, headers, cookies):
        logger.info('downloading %s' % url)
        try:
            if not gfw:
                async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
                    # 设置随机爬取间隔
                    time.sleep(random.randint(1, 3) + random.random())
                    async with session.get(url, ssl=False) as r:
                        code = r.status
                        if 200 <= code < 300:
                            if page_type == 'normal':
                                text = await r.text()
                                try:
                                    await eval('parse(text)',
                                               {'parse': eval('self.spider.parse_{}'.format(name)), 'text': text})
                                except Exception:
                                    logger.error('parse_%s error' % name, exc_info=True)
                            else:
                                text = await r.text()
                                try:
                                    await eval('parse(text,api)', {'parse': eval('self.spider.parse_{}'.format(name)),
                                                                   'text': text, 'api': 1})
                                except Exception:
                                    logger.error('parse_%s error' % name, exc_info=True)
                        else:
                            logger.error('page %s failed, status code: %s' % (url, code), exc_info=True)
            else:
                async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
                    # 设置随机爬取间隔
                    time.sleep(random.randint(1, 3) + random.random())
                    async with session.get(url, proxy=GFW_PROXY, ssl=False) as r:
                        code = r.status
                        if 200 <= code < 300:
                            if page_type == 'normal':
                                text = await r.text()
                                try:
                                    await eval('parse(text)',
                                               {'parse': eval('self.spider.parse_{}'.format(name)), 'text': text})
                                except Exception:
                                    logger.error('parse_%s error' % name, exc_info=True)
                            else:
                                text = await r.text()
                                try:
                                    await eval('parse(text,api)', {'parse': eval('self.spider.parse_{}'.format(name)),
                                                                   'text': text, 'api': page_type})
                                except Exception:
                                    logger.error('parse_%s error' % name, exc_info=True)
                        else:
                            logger.error('page %s failed, status code: %s' % (url, code), exc_info=True)
        except (ClientConnectionError, ClientHttpProxyError, ClientProxyConnectionError,
                CancelledError, Exception):
            logger.error('page %s failed' % url, exc_info=True)