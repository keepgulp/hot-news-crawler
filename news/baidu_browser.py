#!/usr/bin/env python3
"""
百度热搜爬虫 - 使用浏览器方案
"""
import subprocess
import json
import re
from typing import List, Dict


def get_baidu_hot() -> List[Dict]:
    """通过浏览器获取百度热搜"""
    data = []
    try:
        # 使用 playwright 或直接用 curl + selenium
        # 这里用简化版：调用 node 执行浏览器
        result = subprocess.run([
            'node', '-e', '''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://top.baidu.com/board?tab=realtime', {timeout: 15000});
  await page.waitForTimeout(3000);
  const text = await page.evaluate(() => document.body.innerText);
  console.log(text);
  await browser.close();
})();
'''
        ], capture_output=True, text=True, timeout=30, cwd='/root/.openclaw/mainworkspace/hot-news-crawler')
        
        text = result.stdout
        # 解析热搜数据
        lines = text.split('\n')
        i = 0
        current_rank = 0
        current_title = ""
        current_hot = ""
        
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+$', line) and 1 <= int(line) <= 50:
                if current_title:
                    data.append({
                        'title': current_title,
                        'url': f"https://www.baidu.com/s?wd={current_title}",
                        'hot': current_hot
                    })
                current_rank = int(line)
                current_title = ""
                current_hot = ""
            elif '热搜指数' in line and i > 0:
                # 上一行是热度值
                pass
            elif line and not current_title and '查看更多' not in line and '热搜指数' not in line and len(line) > 2:
                if not re.match(r'^\d+$', line):
                    current_title = line
        
        # 添加最后一条
        if current_title:
            data.append({
                'title': current_title,
                'url': f"https://www.baidu.com/s?wd={current_title}",
                'hot': current_hot
            })
            
    except Exception as e:
        print(f"[Baidu Browser Error] {e}")
    return data[:20]


if __name__ == '__main__':
    print("=== 百度热搜 (浏览器) ===")
    for i, item in enumerate(get_baidu_hot()[:10], 1):
        print(f"{i}. {item['title']}")
