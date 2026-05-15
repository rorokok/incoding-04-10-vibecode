import urllib.request
import urllib.parse
import json
import datetime
import re

def get_jaun_meals(date=None):
    """
    자운고등학교의 급식 정보를 가져옵니다.
    date: 'YYYYMMDD' 형식의 문자열 (예: '20231024'). 입력하지 않으면 오늘 날짜를 사용합니다.
    """
    # API 기본 정보
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    
    # 자운고등학교 코드 정보
    params = {
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": "B10",  # 서울특별시교육청
        "SD_SCHUL_CODE": "7010703",   # 자운고등학교
    }
    
    # 날짜 설정 (기본값: 오늘)
    if date is None:
        today = datetime.datetime.now()
        date = today.strftime("%Y%m%d")
    
    params["MLSV_YMD"] = date
    
    # 파라미터를 URL에 인코딩하여 붙임
    query_string = urllib.parse.urlencode(params)
    request_url = f"{url}?{query_string}"
    
    try:
        # API 요청
        response = urllib.request.urlopen(request_url)
        data = json.loads(response.read())
        
        # 결과 처리
        if "mealServiceDietInfo" in data:
            rows = data["mealServiceDietInfo"][1]["row"]
            print(f"=== {date[:4]}년 {date[4:6]}월 {date[6:]}일 자운고등학교 급식 메뉴 ===")
            
            for row in rows:
                meal_type = row["MMEAL_SC_NM"] # 조식, 중식, 석식 등
                menu = row["DDISH_NM"]         # 급식 메뉴
                
                # 메뉴에 포함된 알레르기 정보 숫자 및 특수문자 제거 (깔끔하게 출력하기 위해)
                clean_menu = re.sub(r'[0-9.*]+<br/>', '\n', menu) # <br/> 태그를 줄바꿈으로 변경
                clean_menu = re.sub(r'<br/>', '\n', clean_menu)
                clean_menu = re.sub(r'[^가-힣a-zA-Z\s\n]', '', clean_menu)
                
                # 여러 번의 공백이나 빈 줄 정리
                clean_menu = '\n'.join([line.strip() for line in clean_menu.split('\n') if line.strip()])
                
                print(f"\n[{meal_type}]")
                print(clean_menu)
                
        else:
            # 급식 정보가 없는 경우 (RESULT 딕셔너리 확인)
            if "RESULT" in data and data["RESULT"]["CODE"] == "INFO-200":
                print(f"{date[:4]}년 {date[4:6]}월 {date[6:]}일은 급식 정보가 없습니다.")
            else:
                print("데이터를 불러오는 중 문제가 발생했습니다:", data)
                
    except Exception as e:
        print("API 호출 중 오류가 발생했습니다:", e)

if __name__ == "__main__":
    print("자운고등학교 급식 알리미 프로그램입니다.")
    print("---------------------------------------")
    
    while True:
        choice = input("1. 오늘 급식 보기\n2. 특정 날짜 급식 보기\n3. 종료\n선택해주세요 (1/2/3): ")
        
        if choice == '1':
            get_jaun_meals()
            print("\n---------------------------------------")
        elif choice == '2':
            target_date = input("날짜를 입력해주세요 (예: 20240515): ")
            if len(target_date) == 8 and target_date.isdigit():
                get_jaun_meals(target_date)
            else:
                print("잘못된 날짜 형식입니다. 8자리 숫자로 입력해주세요.")
            print("\n---------------------------------------")
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")
            print("\n---------------------------------------")
