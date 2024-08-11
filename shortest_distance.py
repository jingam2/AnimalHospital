import random
import geopandas as gpd
from shapely.geometry import Point
import folium

# 어플로부터 받은 위치 정보 (예: 사용자가 선택한 위치)
start_lat = random.uniform(34, 38)
start_lng = random.uniform(126, 131)

# CSV 파일을 Geopandas 데이터프레임으로 읽어오기
csv_file_path = 'data/latlng_of_hospital.csv'
gdf = gpd.read_file(csv_file_path, encoding='utf-8')

# 시작 지점 좌표 생성
start_point = Point(start_lng, start_lat)

# 각 병원의 좌표를 활용하여 최단거리 계산
def calculate_distance(row):
    end_point = Point(row['longitude'], row['latitude'])
    return start_point.distance(end_point)

# 각 병원에 대해 최단거리 계산 후 새로운 열에 추가
gdf['shortest_distance'] = gdf.apply(calculate_distance, axis=1)

# NaN 값을 가지는 행 제거
gdf = gdf.dropna(subset=['shortest_distance'])

if not gdf.empty:
    # 가장 가까운 병원 정보 찾기
    nearest_place = gdf.loc[gdf['shortest_distance'].idxmin()]

    print("가장 가까운 병원 정보:")
    print("병원 이름:", nearest_place['hospital_name'])
    print("병원 주소:", nearest_place['hospital_addr'])
    print("병원 번호:", nearest_place['hospital_number'])

    # 폴리움 지도 생성
    m = folium.Map(location=[start_lat, start_lng], zoom_start=13)

    # 시작 위치 마커 추가
    folium.Marker([start_lat, start_lng], popup="시작 위치").add_to(m)

    # 가장 가까운 병원 위치 마커 추가 (파란색 별모양 아이콘)
    popup_content = f"병원 이름 : {nearest_place['hospital_name']},전화번호 : {nearest_place['hospital_number']}"
    folium.Marker(
        [nearest_place['latitude'], nearest_place['longitude']],
        icon=folium.Icon(icon='star', color='red'),
        popup=folium.Popup(popup_content,max_width=600)
    ).add_to(m)

    # 폴리움 지도 저장
    map_file_path = 'nearest_hospital_map.html'
    m.save(map_file_path)

    print("폴리움 지도가 생성되었습니다. 파일명:", map_file_path)
else:
    print("최단거리를 계산할 병원이 없습니다.")
