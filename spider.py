from utility import Utility
from lxml.html import etree
from rules import rules
from db import RedisClient
import re
import js2py
from tools.logger import logger
import base64


class ProxySpider(Utility):

    def __init__(self):
        self.rules = rules
        self.redis = RedisClient()
        self.spider_running = True
        self.ctx = None

    async def parse_66ip(self, text, api=None):
        logger.info('parsing...')
        protocol = 'http'
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="main"]//table//tr[position()>1]//td[position()<3]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 2):
                ip = li[i]
                port = li[i + 1]
                self.redis.add('66ip-{}://{}:{}'.format(protocol, ip, port))
        else:
            html = etree.HTML(text)
            li = html.xpath('//body//text()')
            for i in range(len(li)):
                if ':' in li[i]:
                    ip_port = li[i].strip('\r\n\r\n \t')
                    self.redis.add('66ip-{}://{}'.format(protocol, ip_port))

    async def parse_ip3366(self, text, api=None):
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="list"]/table/tbody/tr/td[position()<5]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 4):
                ip = li[i]
                port = li[i + 1]
                protocol = li[i + 3].lower()
                self.redis.add('ip3366-{}://{}:{}'.format(protocol, ip, port))

    async def parse_kuaidaili(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="list"]/table/tbody/tr/td[position()<5]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 4):
                ip = li[i]
                port = li[i + 1]
                protocol = li[i + 3].lower()
                self.redis.add('kuaidaili-{}://{}:{}'.format(protocol, ip, port))
        if api == 'proxylist':
            html = etree.HTML(text)
            li = html.xpath('//*[@id="freelist"]/table/tbody/tr/td[position()<5]/text()')
            for i in range(0, len(li), 4):
                ip = li[i]
                port = li[i + 1]
                protocol = li[i + 3].split(',')[0].strip('').lower()
                self.redis.add('kuaidaili-{}://{}:{}'.format(protocol, ip, port))

    async def parse_xicidaili(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="ip_list"]//tr[position()>1]/td[position()<7]')
            # logger.info('li: ', li)
            for i in range(0, len(li), 6):
                ip = li[i + 1].xpath('./text()')[0]
                port = li[i + 2].xpath('./text()')[0]
                protocol = li[i + 5].xpath('./text()')[0].lower()
                self.redis.add('xicidaili-{}://{}:{}'.format(protocol, ip, port))

    async def parse_mrhinkydink(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//tr[@class="text"]/td[position()<3]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 4):
                ip = li[i]
                port = li[i + 1]
                protocol = 'http'
                self.redis.add('mrhinkydink-{}://{}:{}'.format(protocol, ip, port))

    async def parse_ab57(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            li = text.split('\r\n')
            # logger.info('li: ', li)
            for ips in li:
                ip_port = ips
                protocol = 'http'
                self.redis.add('ab57-{}://{}'.format(protocol, ip_port))

    async def parse_proxylists(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            li = text.split('\r\n')
            # logger.info('li: ', li)
            for ips in li:
                ip_port = ips
                protocol = 'http'
                self.redis.add('proxylists-{}://{}'.format(protocol, ip_port))

    async def parse_my_proxy(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@class="list"]/text()')
            # logger.info('li: ', li)
            for ips in li:
                ip_port = re.sub(r'#.*', '', ips)
                protocol = 'http'
                self.redis.add('my_proxy-{}://{}'.format(protocol, ip_port))

    async def parse_rmccurdy(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            li = text.split('\n')
            # logger.info('li: ', li)
            for ips in li:
                if re.match(r'^\d+.*\d+$', ips):
                    ip_port = ips
                    protocol = 'http'
                    self.redis.add('rmccurdy-{}://{}'.format(protocol, ip_port))

    async def parse_cool_proxy(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="main"]/table//tr[position()>1]')
            self.ctx = js2py.EvalJs()
            for tr_ele in li:
                td_num = len(tr_ele.xpath('.//td'))
                if td_num > 3:
                    ip = await self.get_cool_proxy_ip(tr_ele.xpath('.//td[1]/script/text()')[0])
                    port = tr_ele.xpath('.//td[2]/text()')[0]
                    protocol = 'http'
                    if re.search(r':\d+', ip):
                        self.redis.add('cool_proxy-{}://{}'.format(protocol, ip))
                    else:
                        self.redis.add('cool_proxy-{}://{}:{}'.format(protocol, ip, port))

    async def get_cool_proxy_ip(self, param_text):
        param = re.search(r'str_rot13\(\"(.*)\"\)\)\)', param_text).group(1)
        func_js = '''
            function str_rot13(str) {
                    return (str + '')
                        .replace(/[a-z]/gi, function (s) {
                            return String.fromCharCode(s.charCodeAt(0) + (s.toLowerCase() < 'n' ? 13 : -13));
                        });
                };
        '''
        ip_js = "var ip = str_rot13('%s')" % param
        final_js = ''.join([func_js, ip_js])
        self.ctx.execute(final_js)
        base_ip = self.ctx.ip
        ip_str = base64.b64decode(base_ip.encode()).decode()
        ip = re.sub(r'#.*', '', ip_str)
        return ip

    async def parse_goubanjia(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="services"]//div[@class="span12"]//tbody/tr')
            for tr_ele in li:
                ip_li = tr_ele.xpath('./td[1]/*[not(contains(@style,"display: none;"))]/text()')
                ip_port = ''.join(ip_li[:-1] + [':'] + [ip_li[-1]])
                protocol = tr_ele.xpath('./td[3]/a/text()')[0]
                self.redis.add('goubanjia-{}://{}'.format(protocol, ip_port))

    async def parse_cn_proxy(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//table[@class="sortable"]/tbody/tr/td[position()<3]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 2):
                ip = li[i]
                port = li[i + 1]
                protocol = 'http'
                self.redis.add('cn_proxy-{}://{}:{}'.format(protocol, ip, port))

    async def parse_xroxy(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[position()<3]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 2):
                ip = li[i]
                port = li[i + 1]
                protocol = 'http'
                self.redis.add('xroxy-{}://{}:{}'.format(protocol, ip, port))

    async def parse_proxylistplus(self, text, api=None):
        logger.info('parsing...')
        if api is None:
            html = etree.HTML(text)
            li = html.xpath('//*[@id="page"]/table[2]//tr[position()>2]/td[position()<4]/text()')
            # logger.info('li: ', li)
            for i in range(0, len(li), 2):
                ip = li[i]
                port = li[i + 1]
                protocol = 'http'
                self.redis.add('proxylistplus-{}://{}:{}'.format(protocol, ip, port))
