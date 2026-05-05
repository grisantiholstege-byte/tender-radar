import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def fetch_guizhou_public():
    """提取贵州招标投标公共服务平台的印刷包装类公告"""
    url = "http://ztb.guizhou.gov.cn/trade/bulletin/?pageNo=1&pageSize=20"
    headers = {"User-Agent": "Mozilla/5.0"}
    items = []
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for li in soup.select('ul.news-list li'):
            title_el = li.select_one('a.title')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            # 只保留包装、印刷、酒盒等关键词
            if not any(kw in title for kw in ['包装','印刷','酒盒','礼盒','手提袋','出版物','商务印刷','纸箱','标签']):
                continue
            date_el = li.select_one('span.date')
            pub_date = date_el.get_text(strip=True) if date_el else ''
            href = title_el.get('href', '')
            if href and not href.startswith('http'):
                href = 'http://ztb.guizhou.gov.cn' + href
            items.append({
                "name": title,
                "company": "（需进入公告查看）",
                "type": "包装印刷",
                "pubDate": pub_date,
                "deadline": "详见公告",
                "status": "招标中",
                "keyword": "",
                "region": "贵州",
                "platform": "贵州招标投标公共服务平台",
                "refUrl": href
            })
    except Exception as e:
        print("贵州平台抓取出错：", e)
    return items

def main():
    all_data = []
    all_data.extend(fetch_guizhou_public())
    # 可以继续添加其他平台（例如黔云招采），格式同上
    # 如果没有抓到内容，保留上一次的数据（检查文件是否存在）
    if not all_data:
        print("⚠️ 本次未抓取到任何项目，data.json 保持不变")
        return
    # 保存为 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功抓取 {len(all_data)} 条招标信息")

if __name__ == '__main__':
    main()
