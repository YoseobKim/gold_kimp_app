const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');

// 데이터 저장 디렉토리 생성
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR);
}

const targets = [
    {
        name: 'live_gold.json',
        url: 'https://data-asg.goldprice.org/dbXRates/USD',
        headers: { 'Referer': 'https://goldprice.org/', 'User-Agent': 'Mozilla/5.0' }
    },
    {
        name: 'live_fx.json',
        url: 'https://api.manana.kr/exchange/rate/KRW/USD.json'
    },
    {
        name: 'gold_series.json',
        url: 'https://goldkimp.com/wp-content/uploads/json/gold_premium_series.json'
    },
    {
        name: 'gold_kimp_latest.json',
        url: 'https://goldkimp.com/wp-json/gk/gold/v1?tf=15m'
    }
];

async function updateAllData() {
    console.log(`데이터 수집 시작: ${new Date().toISOString()}`);

    for (const target of targets) {
        try {
            const response = await fetch(target.url, { headers: target.headers || {} });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            fs.writeFileSync(path.join(DATA_DIR, target.name), JSON.stringify(data, null, 2));
            console.log(`✅ 성공: ${target.name}`);
        } catch (error) {
            console.error(`❌ 실패: ${target.name} - ${error.message}`);
        }
    }
}

updateAllData();
