#!/usr/bin/env python3
"""
热点资讯爬虫 - 主程序
"""
from news.crawler import NewsAggregator
import argparse
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='热点资讯爬虫')
    parser.add_argument('--output', '-o', default=None, help='输出文件路径')
    parser.add_argument('--source', '-s', nargs='+', 
                        choices=['微博热搜', '知乎热榜', '百度热搜', '科技36kr'],
                        help='指定爬取来源')
    args = parser.parse_args()
    
    aggregator = NewsAggregator()
    
    # 如果指定了来源，只爬取指定的
    if args.source:
        aggregator.crawlers = {k: v for k, v in aggregator.crawlers.items() if k in args.source}
    
    news = aggregator.get_all_news()
    
    # 打印结果
    print("\n" + "="*50)
    print(f"📰 热点资讯汇总 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    for source, items in news.items():
        print(f"\n🔥 {source}")
        for i, item in enumerate(items[:10], 1):
            print(f"  {i}. {item.get('title', '')[:50]}")
    
    # 保存到文件
    output_file = args.output or f"hot_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存到: {output_file}")


if __name__ == '__main__':
    main()
