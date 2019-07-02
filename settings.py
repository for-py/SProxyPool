TEST_URL = 'https://www.baidu.com'

# 自行配置的检验代理匿名性接口，若不配置，默认为None
ANON_CHECK_API = ''

# check the anonymity of proxy
ANON_CHECK_URL = ANON_CHECK_API or 'http://httpbin.org/ip'

# Redis数据库地址，需提前安装、配置、启动redis
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0

# 配置初始分数，验证次数，有效代理分值，无效代理分值界限
INITIAL_SCORE = 60
# 验证次数
VALIDATE_TIME = 1
# 通过验证的代理分值
VALIDATED_SCORE = 100
# 低于此分值的代理被丢弃
DISCARD_SCORE = 0

# 维护的有效代理数量
VALIDATED_PROXY_NUM = 3000

VALID_STATUS_CODES = [200, 302]

# GFW代理
GFW_PROXY = 'http://127.0.0.1:8001'

# redis key
PROXY_ORIGINAL = 'proxy:original'
PROXY_VALIDATED = 'proxy:validated'

# 待用的redis key，自定义，比如用于CSDN的代理
PROXY_FOR_USE = 'proxy:for:use'

# concurrency task num
CONCURRENCY_TASK_LIMIT = 30

# spider running signal
SPIDER_RUNNING = True
