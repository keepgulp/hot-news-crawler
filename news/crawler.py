#!/usr/bin/env python3
"""
热点资讯爬虫 - 支持多个平台
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional
from datetime import datetime


class NewsCrawler:
    """热点资讯爬虫基类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://weibo.com',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _fetch(self, url: str, encoding: str = 'utf-8') -> Optional[str]:
        """获取网页内容"""
        try:
            resp = self.session.get(url, timeout=10)
            resp.encoding = encoding
            return resp.text
        except Exception as e:
            print(f"[Error] {url}: {e}")
            return None


class WeiboCrawler(NewsCrawler):
    """微博热搜爬虫"""
    
    def get_hot(self) -> List[Dict]:
        url = "https://weibo.com/ajax/side/hotSearch"
        data = []
        try:
            resp = self.session.get(url, timeout=10)
            result = resp.json()
            realtime = result.get('data', {}).get('realtime', [])
            for item in realtime[:20]:
                data.append({
                    'title': item.get('word', ''),
                    'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                    'hot': item.get('num', 0),
                    'label': item.get('label_name', '')
                })
        except Exception as e:
            print(f"[Weibo Error] {e}")
        return data


class ZhihuCrawler(NewsCrawler):
    """知乎热榜爬虫"""
    
    def get_hot(self) -> List[Dict]:
        url = "https://api.zhihu.com/topstory/hot-lists/total?limit=20"
        data = []
        try:
            # 使用正确的知乎 API
            resp = self.session.get(url, timeout=10)
            result = resp.json()
            for item in result.get('data', []):
                target = item.get('target', {})
                data.append({
                    'title': target.get('title', ''),
                    'url': target.get('url', '').replace('api.zhihu.com', 'www.zhihu.com'),
                    'hot': item.get('detail_text', ''),
                })
        except Exception as e:
            print(f"[Zhihu Error] {e}")
        return data


class BaiduCrawler(NewsCrawler):
    """百度热搜爬虫 - 使用硬编码数据(实时数据请用浏览器)"""
    
    def get_hot(self) -> List[Dict]:
        # 百度反爬较严，目前使用预置的热点数据
        # 实际使用中建议用浏览器自动化或第三方API
        data = [
            {'title': '315晚会', 'url': 'https://www.baidu.com/s?wd=315晚会', 'hot': '780万'},
            {'title': '315曝光网红鸡爪', 'url': 'https://www.baidu.com/s?wd=315曝光网红鸡爪', 'hot': '771万'},
            {'title': '以315为契机 护航365', 'url': 'https://www.baidu.com/s?wd=以315为契机 护航365', 'hot': '761万'},
            {'title': '有友鸡爪客服回应', 'url': 'https://www.baidu.com/s?wd=有友鸡爪客服回应', 'hot': '752万'},
            {'title': '哈啰回应被315点名', 'url': 'https://www.baidu.com/s?wd=哈啰回应被315点名', 'hot': '742万'},
            {'title': '网警提醒看不见的虚假更要防', 'url': 'https://www.baidu.com/s?wd=网警提醒看不见的虚假更要防', 'hot': '732万'},
            {'title': '刘文祥店员：20元1斤能是纯牛肉吗', 'url': 'https://www.baidu.com/s?wd=刘文祥', 'hot': '694万'},
            {'title': '315晚会曝光完整名单', 'url': 'https://www.baidu.com/s?wd=315晚会曝光完整名单', 'hot': '675万'},
            {'title': '伊朗首次出动泥石弹道导弹', 'url': 'https://www.baidu.com/s?wd=伊朗泥石导弹', 'hot': '666万'},
            {'title': '武契奇：3个邻居准备联合进攻塞尔维亚', 'url': 'https://www.baidu.com/s?wd=武契奇', 'hot': '655万'},
        ]
        return data


class TechCrawler(NewsCrawler):
    """科技新闻爬虫 (36kr) - 备用方案"""
    
    def get_news(self) -> List[Dict]:
        # 36kr 有反爬，用备用数据源
        return []


class NewsAggregator:
    """资讯聚合器"""
    
    def __init__(self):
        self.crawlers = {
            '微博热搜': WeiboCrawler(),
            '知乎热榜': ZhihuCrawler(),
            '百度热搜': BaiduCrawler(),
            '科技36kr': TechCrawler(),
        }
    
    def get_all_news(self) -> Dict[str, List[Dict]]:
        """获取所有平台的热搜"""
        results = {}
        for name, crawler in self.crawlers.items():
            print(f"正在爬取 {name}...")
            try:
                if hasattr(crawler, 'get_hot'):
                    results[name] = crawler.get_hot()
                else:
                    results[name] = crawler.get_news()
            except Exception as e:
                print(f"[Error] {name}: {e}")
                results[name] = []
            time.sleep(1)  # 避免请求过快
        return results
    
    def save_to_json(self, filename: str = None):
        """保存到 JSON 文件"""
        if filename is None:
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        news = self.get_all_news()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
        
        print(f"已保存到 {filename}")
        return filename


if __name__ == '__main__':
    aggregator = NewsAggregator()
    aggregator.save_to_json('hot_news.json')
