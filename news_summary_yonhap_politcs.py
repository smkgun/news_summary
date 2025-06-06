# 파이어: app.py
import streamlit as st
from crawler import get_article_info, get_latest_yna_urls
from summarizer import summarize_text
from datetime import datetime, date, time, timedelta
import os
import json

CACHE_FILE = 'article_cache.json'

def load_seen_articles():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_seen_articles(seen_ids):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(seen_ids), f, ensure_ascii=False)

urls = get_latest_yna_urls(limit=30)

st.set_page_config(page_title="정치 뉴스 요약", layout="centered", 
                   initial_sidebar_state="collapsed"
                   )  # 모바일 첫 진입시 사이드바 닫힘
st.title("📰 연합뉴스 정치 뉴스 실시간 요약 ")

if 'last_checked' not in st.session_state:
    st.session_state.last_checked = datetime.now()

col1, col2 = st.sidebar.columns(2)
selected_date = col1.date_input("기준 날짜", value=st.session_state.last_checked.date())
selected_time = col2.time_input("기준 시각", value=st.session_state.last_checked.time())

user_dt = datetime.combine(selected_date, selected_time)
cutoff_dt = datetime.now() - timedelta(days=3)

st.sidebar.caption("※ 최근 3일 이전 기사 데이터는 자동 제거됩니다. 최대 30개 최신 기사를 수집합니다.")

def parse_yna_time(timestr):
    try:
        return datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S")
    except:
        try:
            return datetime.strptime(timestr, "%Y-%m-%d %H:%M")
        except:
            return datetime.now()

if 'seen_articles' not in st.session_state:
    st.session_state.seen_articles = load_seen_articles()

article_infos = []
for url in urls:
    info = get_article_info(url)
    info['url'] = url
    info['article_time'] = parse_yna_time(info['timestamp'])
    info['id'] = url.split('/')[-1]
    if info['article_time'] >= cutoff_dt:
        article_infos.append(info)

# 🔄 최신순 정렬 보장
article_infos.sort(key=lambda x: x['article_time'], reverse=False)

for info in article_infos:
    url = info['url']
    art_id = info['id']
    article_time = info['article_time']
    is_new = art_id not in st.session_state.seen_articles

    st.markdown("---")
    if article_time > user_dt and is_new:
        st.markdown(f"### 🆕 **[{info['title']}]({url})**")
    elif art_id in st.session_state.seen_articles:
        st.markdown(f"### 🧾 **[OLD] [{info['title']}]({url})**")
    else:
        st.markdown(f"#### ✅ [이미 확인한 기사] [{info['title']}]({url})")

    st.markdown(f"**🕒 송고시각**: {info['timestamp']}")
    st.markdown(f"**📎 부제**: {info['subtitle']}")
    with st.expander("요약 보기"):
        st.write(summarize_text(info['content'], lead=info.get('lead', '')))

    if is_new:
        st.session_state.seen_articles.add(art_id)

save_seen_articles(st.session_state.seen_articles)

st.caption("마지막 업데이트: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

with st.sidebar:
    st.markdown("---")
    st.markdown("<sub>Powered by Data-Insight LAB 'IF'</sub>", unsafe_allow_html=True)
