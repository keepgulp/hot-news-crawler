#!/usr/bin/env python3
"""
测试用例
"""
import unittest
from news.crawler import WeiboCrawler, BaiduCrawler, NewsAggregator


class TestCrawlers(unittest.TestCase):
    """爬虫测试"""
    
    def test_weibo(self):
        """测试微博热搜"""
        crawler = WeiboCrawler()
        result = crawler.get_hot()
        self.assertIsInstance(result, list)
        print(f"微博热搜: 获取到 {len(result)} 条")
    
    def test_baidu(self):
        """测试百度热搜"""
        crawler = BaiduCrawler()
        result = crawler.get_hot()
        self.assertIsInstance(result, list)
        print(f"百度热搜: 获取到 {len(result)} 条")
    
    def test_aggregator(self):
        """测试聚合器"""
        aggregator = NewsAggregator()
        result = aggregator.get_all_news()
        self.assertIsInstance(result, dict)
        print(f"聚合结果: {len(result)} 个来源")


if __name__ == '__main__':
    unittest.main()
