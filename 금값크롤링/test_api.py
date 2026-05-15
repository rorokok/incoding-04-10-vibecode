import urllib.request
import urllib.parse
import json
import datetime
from datetime import timedelta

end_date = datetime.datetime.now()
start_date = end_date - timedelta(days=365)

url = 'https://koreagoldx.co.kr/api/price/chart/list'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json'
}

data = {
    'srchDt': '1Y',
    'type': 'Au',
    'dataDateStart': start_date.strftime('%Y.%m.%d'),
    'dataDateEnd': end_date.strftime('%Y.%m.%d')
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    
    print(f"Number of items: {len(result.get('list', []))}")
    if len(result.get('list', [])) > 0:
        print(f"Sample item: {result['list'][0]}")
    else:
        print("Empty list returned. Trying without srchDt...")
        
        # Try without srchDt
        data2 = {
            'type': 'Au',
            'dataDateStart': start_date.strftime('%Y.%m.%d'),
            'dataDateEnd': end_date.strftime('%Y.%m.%d')
        }
        req2 = urllib.request.Request(url, data=json.dumps(data2).encode('utf-8'), headers=headers)
        response2 = urllib.request.urlopen(req2)
        result2 = json.loads(response2.read().decode('utf-8'))
        print(f"Number of items (no srchDt): {len(result2.get('list', []))}")
        if len(result2.get('list', [])) > 0:
            print(f"Sample item: {result2['list'][0]}")
            
except Exception as e:
    print(f"Error: {e}")
