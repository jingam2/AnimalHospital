import pandas as pd

# CSV 파일을 데이터프레임으로 읽어오기
csv_file_path = 'data/latlng_of_hospital.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

# 결측값 개수 확인
missing_values_count = df.isnull().sum()
print("결측값 개수:")
print(missing_values_count)

# 결측값이 있는 행의 위치 출력
missing_rows = df[df.isnull().any(axis=1)]
missing_rows.index = missing_rows.index + 2  # 인덱스에 +2를 csv파일에 맞게
print("결측값이 있는 행의 위치:")
print(missing_rows)
