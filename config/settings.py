"""
配置中心
"""

# 爬虫配置
CRAWLER_CONFIG = {
    'timeout': 10,
    'retry': 3,
    'delay': 1,  # 请求间隔(秒)
    'max_items': 20,  # 每个来源最多获取条数
}

# 输出配置
OUTPUT_CONFIG = {
    'format': 'json',  # json, markdown, html
    'save_dir': './output',
}

# 定时任务配置
CRON_CONFIG = {
    'enabled': True,
    'time': '09:00',  # 每天9点执行
    'sources': ['微博热搜', '知乎热榜', '百度热搜', '科技36kr'],
}

# 平台配置
PLATFORMS = {
    'weibo': {
        'name': '微博热搜',
        'enabled': True,
    },
    'zhihu': {
        'name': '知乎热榜', 
        'enabled': True,
    },
    'baidu': {
        'name': '百度热搜',
        'enabled': True,
    },
    '36kr': {
        'name': '科技36kr',
        'enabled': True,
    },
}
