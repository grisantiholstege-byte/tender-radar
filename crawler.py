import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 目标关键词
keywords = ['包装', '印刷', '酒盒', '礼盒', '手提袋', '出版物', '商务印刷', '纸箱', '标签', '瓶盖', '彩盒']

def fetch_guizhou_public():
    """贵州招标投标公共服务平台"""
    items = []
    try:
        url = "http://ztb.guizhou.gov.cn/trade/bulletin/?pageNo=1&pageSize=20"
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for li in soup.select('ul.news-list li'):
            title_el = li.select_one('a.title')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not any(kw in title for kw in keywords):
                continue
            date_el = li.select_one('span.date')
            pub_date = date_el.get_text(strip=True) if date_el else ''
            href = title_el.get('href', '')
            if href and not href.startswith('http'):
                href = 'http://ztb.guizhou.gov.cn' + href
            items.append({
                "name": title,
                "company": "（详见公告）",
                "type": guess_type(title),
                "pubDate": pub_date,
                "deadline": "详见公告",
                "status": "招标中",
                "keyword": "",
                "region": "贵州",
                "platform": "贵州招标投标公共服务平台",
                "refUrl": href
            })
        print(f"贵州平台抓取到 {len(items)} 条")
    except Exception as e:
        print("贵州平台抓取出错：", e)
    return items

def fetch_qianyun():
    """黔云招采"""
    items = []
    try:
        url = "https://www.e-qyzc.com/trade/bulletin/?pageNo=1&pageSize=20"
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for li in soup.select('ul.news-list li'):
            title_el = li.select_one('a.title')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not any(kw in title for kw in keywords):
                continue
            date_el = li.select_one('span.date')
            pub_date = date_el.get_text(strip=True) if date_el else ''
            href = title_el.get('href', '')
            if href and not href.startswith('http'):
                href = 'https://www.e-qyzc.com' + href
            items.append({
                "name": title,
                "company": "（详见公告）",
                "type": guess_type(title),
                "pubDate": pub_date,
                "deadline": "详见公告",
                "status": "招标中",
                "keyword": "",
                "region": "贵州",
                "platform": "黔云招采",
                "refUrl": href
            })
        print(f"黔云招采抓取到 {len(items)} 条")
    except Exception as e:
        print("黔云招采抓取出错：", e)
    return items

def fetch_moutai_wenlv():
    """茅台文旅官网（供应商招募公告）"""
    items = []
    try:
        url = "https://www.mtwhly.com/mtwhly/xwzx54/gggs86/index.html"
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for li in soup.select('ul.news-list li'):
            title_el = li.select_one('a.title')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not any(kw in title for kw in ['供应商', '招募', '入库', '包装', '礼盒', '酒盒', '印刷', '手提袋']):
                continue
            date_el = li.select_one('span.date')
            pub_date = date_el.get_text(strip=True) if date_el else ''
            href = title_el.get('href', '')
            if href and not href.startswith('http'):
                href = 'https://www.mtwhly.com' + href
            items.append({
                "name": title,
                "company": "茅台文旅",
                "type": "供应商招募",
                "pubDate": pub_date,
                "deadline": "详见公告",
                "status": "招募中",
                "keyword": "",
                "region": "仁怀",
                "platform": "茅台文旅",
                "refUrl": href
            })
        print(f"茅台文旅抓取到 {len(items)} 条")
    except Exception as e:
        print("茅台文旅抓取出错：", e)
    return items

def guess_type(title):
    """根据标题自动分类"""
    if any(k in title for k in ['酒盒','礼盒','手提袋','瓶盖','酒瓶']):
        return "酒类包装"
    elif any(k in title for k in ['出版物','图书','教材','报纸']):
        return "出版物印刷"
    elif any(k in title for k in ['食品','粽子','茶叶','刺梨','老干妈']):
        return "食品包装"
    elif any(k in title for k in ['商务','办公','宣传物料','表单']):
        return "商务印刷"
    else:
        return "包装印刷"

def main():
    all_data = []
    all_data.extend(fetch_guizhou_public())
    all_data.extend(fetch_qianyun())
    all_data.extend(fetch_moutai_wenlv())

    if not all_data:
        print("本次未抓取到任何项目，data.json 保持不变")
        return

    # 去重（相同链接只保留一个）
    seen = set()
    unique = []
    for item in all_data:
        if item['refUrl'] in seen:
            continue
        seen.add(item['refUrl'])
        unique.append(item)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功抓取 {len(unique)} 条招标信息")

if __name__ == '__main__':
    main()
