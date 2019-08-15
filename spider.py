"""
批量获取待测ip的"挖掘机"
    - ProxyMetaClass作为ProxyMetaClass的元类， 是为了能够动态地生成两个和爬取免费ip的方法有关；
    - Crawler类主要定义了一组以crawl_打头的爬取方法，并通过调用主方法get_proxies， 遍历上述爬取方法，
        批量爬取一系列proxies，生成的未经有效性检测的ip代理。
"""

import re
import sys

from config import POOL_UPPER_THRESHOLD
from db import RedisClient
from test_proxy_vaild import test_proxy_vaild
from utils import get_page
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from config import *
#import pyquery as pq


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')


# 自定义元类
class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

#爬虫类
class Crawler(object, metaclass=ProxyMetaClass):
    """代理池爬虫封装， 支持多个网站的用户代理"""

    def get_proxies(self, callback):
        for proxy in eval("self.{}()".format(callback)):
            yield proxy

    
    def crawl_xicidaili(self):
        """爬取西刺网站的用户代理"""
        print("西刺".center(100,'*'))
        for page in range(1, 10):  # 获取前5页的信息
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)  # 构建网址
            html = get_page(start_url)  # 获取网页内容
            if html:  # 如果获取成功， 则提取ip和端口
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    # 提取ip的正则表达式
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    # 提取端口的正则表达式
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        # 用冒号拼接IP和端口# str
                        address_port = address + ':' + port
                        # 返回生成器
                        yield address_port.replace(' ', '')

    def crawl_iphai(self):
        for page in range(10):
            start_url = 'http://www.iphai.com/free/%s' % (page)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(str(html))
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        print(address_port)
                        yield address_port.replace(' ', '')



#代理池
class PoolGetter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
         判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def test_proxy_add(self, proxy):
        """检测是否可用， 可用添加到redis中"""
        if test_proxy_vaild(proxy):
            # print('[+]' + proxy + "可用")
            print(Fore.GREEN + '成功获取到代理', proxy)
            self.redis.add(proxy)

    def run(self):
        print("[-] 代理池获取器开始执行......")
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                # 刷新输出
                sys.stdout.flush()
                with ThreadPoolExecutor(ThreadCount) as pool:
                    pool.map(self.test_proxy_add, proxies)

#def is_crawler_ok():
#    crawler =Crawler()
#    for callback_label in range(crawler.__CrawFuncCount__):


def is_pool_ok():
    proxyPool =PoolGetter()
    proxyPool.run()
    print("proxy count:",proxyPool.redis.count())
if __name__ == '__main__':
    # crawler =Crawler()
    # for callback_lable in range(crawler.__CrawFuncCount__):
    #     callback =crawler.__CrowlFunc__[callback_lable]
    #     #获取代理
    #     proxies =crawler.get_proxies(callback)
    #     for item in proxies:
    #         print(item)
    is_pool_ok()