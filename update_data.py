import cloudscraper
import json
import os
import time

DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 1. 스크래퍼 생성 및 초기 설정
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

# 2. GoldPrice.org의 세션을 획득하기 위해 메인 페이지를 먼저 방문합니다. (핵심)
try:
    print("메인 페이지 방문하여 세션 확보 중...")
    scraper.get("https://goldprice.org/", timeout=20)
except:
    pass

targets = [
    {
        "name": "live_gold.json",
        "url": "https://data-asg.goldprice.org/dbXRates/USD",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://goldprice.org/",
            "Origin": "https://goldprice.org",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }
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
        # 3. 요청 시 headers 인자를 명시적으로 전달
        response = scraper.get(target["url"], headers=target["headers"], timeout=20)
        
        if response.status_code == 200:
            with open(os.path.join(DATA_DIR, target["name"]), 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
            print(f"✅ 성공: {target['name']}")
        else:
            print(f"❌ 실패: {target['name']} - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ 에러 발생: {target['name']} - {str(e)}")

print("--- 데이터 수집 종료 ---")
