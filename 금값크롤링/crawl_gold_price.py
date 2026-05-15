import urllib.request
import json
import datetime
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 윈도우에서 한글 폰트 설정 (맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def fetch_gold_prices():
    end_date = datetime.datetime.now()
    start_date = end_date - timedelta(days=365)

    url = 'https://koreagoldx.co.kr/api/price/chart/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }

    data = {
        'srchDt': '1Y',
        'type': 'Au',
        'dataDateStart': start_date.strftime('%Y.%m.%d'),
        'dataDateEnd': end_date.strftime('%Y.%m.%d')
    }

    print("데이터를 가져오는 중입니다...")
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    
    return result.get('list', [])

def process_and_save(data):
    if not data:
        print("데이터가 없습니다.")
        return

    # 데이터프레임으로 변환
    df = pd.DataFrame(data)
    
    # date 컬럼을 datetime 객체로 변환
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date') # 시간순 정렬
    
    # CSV로 저장 (엑셀에서 열 수 있도록 utf-8-sig 사용)
    csv_filename = 'gold_price_1year.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"CSV 파일 저장 완료: {csv_filename}")
    
    # 그래프 그리기 (순금 살 때, 팔 때)
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['s_pure'], label='내가 살 때 (순금)', color='red')
    plt.plot(df['date'], df['p_pure'], label='내가 팔 때 (순금)', color='blue')
    
    plt.title('최근 1년 금 시세 (순금 3.75g 기준)')
    plt.xlabel('날짜')
    plt.ylabel('가격 (원)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # x축 날짜 포맷 최적화
    plt.gcf().autofmt_xdate()
    
    png_filename = 'gold_price_chart.png'
    plt.savefig(png_filename, dpi=300, bbox_inches='tight')
    print(f"그래프 이미지 저장 완료: {png_filename}")

if __name__ == '__main__':
    try:
        price_data = fetch_gold_prices()
        process_and_save(price_data)
        print("모든 작업이 완료되었습니다.")
    except Exception as e:
        print(f"에러 발생: {e}")
