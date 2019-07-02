rules = [
    {
        'name': '66ip',
        'resources': ['http://www.66ip.cn/%s.html' % i for i in range(1, 10)],
        'referer': 'http://www.66ip.cn',
        'host': 'www.66ip.cn',
        'AntiCrawl': True,
        'type': 'normal',
        'GFW': False,
    }, {
        'name': '66ip',
        'resources': ['http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=4&start=&'
                      'ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'],
        'referer': 'http://www.66ip.cn',
        'host': 'www.66ip.cn',
        'AntiCrawl': True,
        'type': 'api',
        'GFW': False
    }, {
        'name': 'ip3366',
        'resources': ['http://www.ip3366.net/free/?stype=1&page=%s' % i for i in range(1, 8)],
        'referer': 'http://www.ip3366.net',
        'host': 'www.ip3366.net',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'kuaidaili',
        'resources': ['https://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, 10)],
        'referer': 'https://www.kuaidaili.com',
        'host': 'www.kuaidaili.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'kuaidaili',
        'resources': ['https://www.kuaidaili.com/ops/proxylist/%s/' % i for i in range(1, 10)],
        'referer': 'https://www.kuaidaili.com',
        'host': 'www.kuaidaili.com',
        'AntiCrawl': False,
        'type': 'proxylist',
        'GFW': False
    },
    {
        'name': 'xicidaili',
        'resources': ['https://www.xicidaili.com/nn/%s' % i for i in range(1, 6)],
        'referer': 'https://www.xicidaili.com',
        'host': 'www.xicidaili.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'mrhinkydink',
        'resources': ['http://www.mrhinkydink.com/proxies%s.htm' % i for i in range(2, 15)] +
                     ['http://www.mrhinkydink.com/proxies.htm'],
        'referer': 'http://www.mrhinkydink.com',
        'host': 'www.mrhinkydink.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'ab57',
        'resources': ['http://ab57.ru/downloads/proxyold.txt'],
        'referer': 'http://ab57.ru',
        'host': 'ab57.ru',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'proxylists',
        'resources': ['http://www.proxylists.net/http_highanon.txt'],
        'referer': 'http://www.proxylists.net',
        'host': 'www.proxylists.net',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'my_proxy',
        'resources': ['https://www.my-proxy.com/free-elite-proxy.html',
                      'https://www.my-proxy.com/free-anonymous-proxy.html',
                      'https://www.my-proxy.com/free-proxy-list.html'] +
                     ['https://www.my-proxy.com/free-proxy-list-%s.html' % i for i in range(2, 11)],
        'referer': 'https://www.my-proxy.com',
        'host': 'www.my-proxy.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': True
    },
    {
        'name': 'rmccurdy',
        'resources': ['https://www.rmccurdy.com/scripts/proxy/good.txt'],
        'referer': 'https://www.rmccurdy.com',
        'host': 'www.rmccurdy.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'cool_proxy',
        'resources':
            ['https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s' % i
             for i in range(1, 10)],
        'referer': 'https://www.cool-proxy.net',
        'host': 'www.cool-proxy.net',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'goubanjia',
        'resources': ['http://www.goubanjia.com/'],
        'referer': 'http://www.goubanjia.com',
        'host': 'www.goubanjia.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'cn_proxy',
        'resources': ['https://cn-proxy.com/'],
        'referer': 'https://cn-proxy.com',
        'host': 'cn-proxy.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    },
    {
        'name': 'proxylistplus',
        'resources': ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % i for i in range(1, 8)],
        'referer': 'https://list.proxylistplus.com',
        'host': 'list.proxylistplus.com',
        'AntiCrawl': False,
        'type': 'normal',
        'GFW': False
    }
]

