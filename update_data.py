import cloudscraper
import json
import os
import time

# 저장 디렉토리 설정
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Cloudflare 우회를 위한 스크래퍼 생성
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

targets = [
    {
        "name": "live_gold.json",
        "url": "https://data-asg.goldprice.org/dbXRates/USD",
        "headers": {"Referer": "https://goldprice.org/"}
    },
    {
        "name": "live_fx.json",
        "url": "https://api.manana.kr/exchange/rate/KRW/USD.json",
        "headers": {}
    },
    {
        "name": "gold_series.json",
        "url": "https://goldkimp.com/wp-content/uploads/json/gold_premium_series.json",
        "headers": {"Referer": "https://goldkimp.com/"}
    },
    {
        "name": "gold_kimp_latest.json",
        "url": "https://goldkimp.com/wp-json/gk/gold/v1?tf=15m",
        "headers": {"Referer": "https://goldkimp.com/"}
    }
]

print(f"--- 데이터 수집 시작 ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")

for target in targets:
    try:
        # 스크래퍼를 사용하여 GET 요청
        response = scraper.get(target["url"], headers=target["headers"], timeout=20)
        
        if response.status_code == 200:
            with open(os.path.join(DATA_DIR, target["name"]), 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
            print(f"✅ 성공: {target['name']}")
        else:
            print(f"❌ 실패: {target['name']} - HTTP {response.status_code}")
            # 상세 에러 확인용 (필요시 주석 해제)
            # print(response.text[:200]) 
            
    except Exception as e:
        print(f"⚠️ 에러 발생: {target['name']} - {str(e)}")

print("--- 데이터 수집 종료 ---")
