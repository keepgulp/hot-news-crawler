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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20"
        data = []
        try:
            resp = self.session.get(url, timeout=10)
            result = resp.json()
            for item in result.get('data', []):
                target = item.get('target', {})
                data.append({
                    'title': target.get('title', ''),
                    'url': f"https://www.zhihu.com/question/{target.get('id', '')}",
                    'hot': target.get('detail_text', ''),
                })
        except Exception as e:
            print(f"[Zhihu Error] {e}")
        return data


class BaiduCrawler(NewsCrawler):
    """百度热搜爬虫"""
    
    def get_hot(self) -> List[Dict]:
        url = "https://top.baidu.com/api?cmd=1"
        data = []
        try:
            resp = self.session.get(url, timeout=10)
            result = resp.json()
            for item in result.get('data', [])[:20]:
                data.append({
                    'title': item.get('word', ''),
                    'url': item.get('url', ''),
                    'hot': item.get('hotScore', 0),
                })
        except Exception as e:
            print(f"[Baidu Error] {e}")
        return data


class TechCrawler(NewsCrawler):
    """科技新闻爬虫 (36kr)"""
    
    def get_news(self) -> List[Dict]:
        url = "https://www.36kr.com/information/web news/"
        data = []
        try:
            html = self._fetch(url)
            soup = BeautifulSoup(html, 'lxml')
            articles = soup.select('.article-item-info')[:10]
            for article in articles:
                title = article.select_one('.item-title')
                if title:
                    data.append({
                        'title': title.get_text(strip=True),
                        'url': 'https://www.36kr.com' + title.get('href', ''),
                    })
        except Exception as e:
            print(f"[36kr Error] {e}")
        return data


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
