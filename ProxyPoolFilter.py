

from db import RedisClient
from test_proxy_vaild import test_proxy_vaild
from concurrent.futures import ThreadPoolExecutor
from config import *
#代理池测试
class PoolTester(object):
    def __init__(self):
        ##实例化数据库
        self.redis = RedisClient()

    def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        #test_proxy_vaild作用：测试代理IP是否可用
        if test_proxy_vaild(proxy):
            self.redis.max(proxy)
            print("[+] 代理可用", proxy)
        else:
            self.redis.drop(proxy)
            print("[-] 代理不可用", proxy)

    def run(self):
        """
        测试的主函数
        :return:
        """
        print("测试器开始运行.......")
        try:
            count = self.redis.count()
            print("当前剩余%d个代理" % (count))
            # 使用线程池, 快速检测proxy是否可用
            with ThreadPoolExecutor(FilterThreadCount) as pool:
                #获取全部代理
                pool.map(self.test_single_proxy, self.redis.all())
        except Exception as e:
            print("测试器发生错误", e)

if __name__ == '__main__':
    test =PoolTester()
    test.run()