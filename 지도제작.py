import pandas as pd
import folium
from folium import IFrame
import webbrowser
import math

# 거리 계산 함수 (haversine 공식)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# 중심 좌표 (대구 중심으로 설정)
center_lat = 35.8714
center_lon = 128.6014
radius_km = 5

# 대피소 데이터 불러오기
df = pd.read_csv('shelters.csv')

# 5km 이내 대피소만 필터
df['distance'] = df.apply(lambda r: haversine(center_lat, center_lon, r['위도'], r['경도']), axis=1)
df_filtered = df[df['distance'] <= radius_km]

# 재난종류별 마커 색상
color_dict = {'민방위': 'red', '지진': 'green'}

# 지도 생성 (기본 스타일)
m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='OpenStreetMap')

# 마커 추가
for idx, row in df_filtered.iterrows():
    html = f"""
    <h4>{row['이름']}</h4>
    <img src="{row['이미지링크']}" width="200">
    """
    iframe = IFrame(html, width=220, height=250)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=popup,
        icon=folium.Icon(color=color_dict.get(row['재난종류'], 'blue'))
    ).add_to(m)

# 지도 저장 및 자동 실행
map_file = 'daegu_shelters_basic.html'
m.save(map_file)
webbrowser.open(map_file)
