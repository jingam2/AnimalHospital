from flask import Flask, render_template, request
from flask_cors import CORS
import os
import geopandas as gpd
from shapely.geometry import Point
import folium

app = Flask(__name__, template_folder='templates')
CORS(app) # http 파일 열기 위해

# 프로젝트 루트 디렉토리 경로
project_root = os.path.dirname(os.path.abspath(__file__))

# CSV 파일을 Geopandas 데이터프레임으로 읽어오기
csv_file_path = os.path.join(project_root, 'static', 'latlng_of_hospital.csv')
gdf = gpd.read_file(csv_file_path, encoding='utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 어플로부터 받은 위치 정보 (사용자가 선택한 위치)
        start_lat = float(request.form['latitude'])
        start_lng = float(request.form['longitude'])

        # 시작 지점 좌표 생성
        start_point = Point(start_lng, start_lat)

        # 각 병원의 좌표를 활용하여 최단거리 계산
        def calculate_distance(row):
            end_point = Point(row['longitude'], row['latitude'])
            return start_point.distance(end_point)

        # 각 병원에 대해 최단거리 계산 후 새로운 열에 추가
        gdf['shortest_distance'] = gdf.apply(calculate_distance, axis=1)

        # NaN 값을 가지는 행 제거
        gdf_cleaned = gdf.dropna(subset=['shortest_distance'])

        if not gdf_cleaned.empty:
            # 가장 가까운 병원 정보 찾기
            nearest_place = gdf_cleaned.loc[gdf_cleaned['shortest_distance'].idxmin()]

            # 폴리움 지도 생성
            m = folium.Map(location=[start_lat, start_lng], zoom_start=13)

            # 시작 위치 마커 추가
            folium.Marker([start_lat, start_lng], popup="시작 위치").add_to(m)

            # 가장 가까운 병원 위치 마커 추가 (파란색 별모양 아이콘)
            popup_content = f"병원 이름 : {nearest_place['hospital_name']}<br>전화번호 : {nearest_place['hospital_number']}"
            folium.Marker(
                [nearest_place['latitude'], nearest_place['longitude']],
                icon=folium.Icon(icon='star', color='red'),
                popup=folium.Popup(popup_content, max_width=600)
            ).add_to(m)

            # 폴리움 지도 저장
            map_file_path = 'static/nearest_hospital_map.html'
            m.save(os.path.join(project_root, map_file_path))

            return render_template('index.html', map_file_path=map_file_path)
        else:
            return "최단거리를 계산할 병원이 없습니다."
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
