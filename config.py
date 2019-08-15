# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies_2'

# 代理分数
MAX_SCORE = 3
MIN_SCORE = 0
INITIAL_SCORE = 1

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 250
#爬虫线程池个数
ThreadCount =200
#代理池中线程池的个数
FilterThreadCount=100


# 检查周期 测试周期的设置
TESTER_CYCLE = 10
# 获取周期
GETTER_CYCLE = 30

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 8123

# 开关
TESTER_ENABLED = True #测试
GETTER_ENABLED = True  ##开启一个子进程
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10
