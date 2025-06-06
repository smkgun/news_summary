# 파이일: crawler.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

# ✅ 최신 기사 URL 수집 개선 버전
def get_latest_yna_urls(limit=30):
    base_url = "https://www.yna.co.kr/politics/all"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    res = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    article_divs = soup.select("div[class^='share-data-']")
    links = []

    for div in article_divs:
        url = div.get("data-share-url")
        if url and url.startswith("https://www.yna.co.kr/view/") and url not in links:
            links.append(url)
        if len(links) >= limit:
            break

    return links


def get_article_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title_tag = soup.find('h1', class_='tit') or soup.find('h1', class_='tit01')
    title = title_tag.get_text(strip=True) if title_tag else '[제목 없음]'

    subtitle = ''
    subtitle_block = soup.find('div', class_='tit-sub') or soup.find('div', class_='summary')
    if subtitle_block:
        h2_list = subtitle_block.find_all('h2', class_='tit01')
        subtitle = ' / '.join([h2.get_text(strip=True) for h2 in h2_list])

    dt_meta = soup.find('meta', attrs={'property': 'article:published_time'})
    timestamp = dt_meta['content'] if dt_meta and dt_meta.has_attr('content') else datetime.now().strftime('%Y-%m-%d %H:%M')

    body = soup.find('div', id='articleWrap') or soup.find('div', class_='story-news article')
    if body:
        paragraphs = [p.get_text(strip=True) for p in body.find_all('p') if not p.has_attr('class')]
        content = ' '.join(paragraphs)
    else:
        content = '[내용 없음]'
        paragraphs = []

    lead = ''  # ✅ 리드문 제거: 중복 방지 목적

    return {
        'title': title,
        'subtitle': subtitle,
        'timestamp': timestamp,
        'content': content,
        'lead': lead
    }
