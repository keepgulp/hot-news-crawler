# Hot News Crawler

热点资讯爬取工具，支持多个平台的热搜榜获取。

## 支持的平台

- 微博热搜
- 知乎热榜
- 百度热搜
- 科技新闻 (36kr, 虎嗅等)

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```python
from news.crawler import NewsCrawler

crawler = NewsCrawler()
hot_news = crawler.get_all_news()

for source, news_list in hot_news.items():
    print(f"=== {source} ===")
    for i, news in enumerate(news_list[:10], 1):
        print(f"{i}. {news['title']}")
```

## 定时任务

```bash
# 每天 9 点自动爬取
crontab -e
0 9 * * * cd /path/to/hot-news-crawler && python -m news.main
```

## License

MIT
