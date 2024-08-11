import folium
import pandas as pd

# 저장된 CSV 파일 경로
csv_file_path = 'data/latlng_of_hospital.csv'

# CSV 파일을 데이터프레임으로 읽어오기
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

# 지도 생성
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# 데이터프레임의 각 행을 순회하며 마커 생성
for idx, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker([row['latitude'], row['longitude']], popup=row['hospital_name']).add_to(m)

# 지도를 HTML 파일로 저장
map_html_path = 'map_with_hospitals.html'
m.save(map_html_path)
print(f"Map saved to {map_html_path}")
