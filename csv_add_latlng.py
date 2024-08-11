import pandas as pd
import requests

# CSV 파일을 데이터프레임으로 읽어오기
# None값 위도,경도 주소 적절하게 수정한 csv파일
csv_file_path = 'data/hospital_data.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

# Kakao Maps API 인증키
api_key = '개인 인증키'

# 데이터프레임에서 'hospital_addr' 열을 순회하며 위도와 경도를 추출하는 함수
def getLatLng(address):
    result = ""

    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    header = {'Authorization': 'KakaoAK ' + api_key}

    r = requests.get(url, headers=header)

    if r.status_code == 200:
        json_data = r.json()
        if 'documents' in json_data and len(json_data['documents']) > 0:
            result_address = json_data["documents"][0]["address"]
            latitude = result_address.get("y")
            longitude = result_address.get("x")
            if latitude is not None and longitude is not None:
                return latitude, longitude

    return None, None

# 결과 출력
# 'hospital_addr' 열에서 주소를 추출하여 위도와 경도를 구하고 새로운 열에 추가
df[['latitude', 'longitude']] = df['hospital_addr'].apply(getLatLng).apply(pd.Series)

# 결과 출력
print(df)

# 결과를 새로운 CSV 파일로 저장
output_csv_path = 'data/latlng_of_hospital.csv'
df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print(f"Data saved to {output_csv_path}")