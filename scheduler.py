"""
设置定时任务， 定期检测和获取代理IP的信息
"""
import time
from multiprocessing import Process

from ProxyPoolFilter import PoolTester
from config import *
from db import RedisClient
import telnetlib
from concurrent.futures import ThreadPoolExecutor

from spider import PoolGetter
from api import app
from test_proxy_vaild import test_proxy_vaild

# #代理池测试
# class PoolTester(object):
#     def __init__(self):
#         ##实例数据库
#         self.redis = RedisClient()
#
#     def test_single_proxy(self, proxy):
#         """
#         测试单个代理
#         :param proxy:
#         :return:
#         """
#
#         if test_proxy_vaild(proxy):
#             self.redis.max(proxy)
#             print("[+] 代理可用", proxy)
#         else:
#             self.redis.decrease(proxy)
#             print("[-] 代理不可用", proxy)
#
#     def run(self):
#         """
#         测试的主函数
#         :return:
#         """
#         print("测试器开始运行.......")
#         try:
#             count = self.redis.count()
#             print("当前剩余%d个代理" % (count))
#             # 使用线程池, 快速检测proxy是否可用
#             with ThreadPoolExecutor(100) as pool:
#                 pool.map(self.test_single_proxy, self.redis.all())
#         except Exception as e:
#             print("测试器发生错误", e)


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """定时检测代理IP是否可用？"""
        tester = PoolTester()
        while True:
            print("测试器开始运行....")
            tester.run()
            # 每隔指定时间进行测试
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定期获取代理
        :param cycle:
        :return:
        """
        getter = PoolGetter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):

        print("代理池开始运行......")
        if API_ENABLED:
            print("正在启动API........")
            api_process = Process(target=self.schedule_api)
            api_process.start()

        if TESTER_ENABLED:
            print("正在启动TESTER.......")
            test_process = Process(target=self.schedule_tester)
            test_process.start()

        if GETTER_ENABLED:
            print("正在启动GETTER......")
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

if __name__ == '__main__':
    test =Scheduler()
    test.run()
