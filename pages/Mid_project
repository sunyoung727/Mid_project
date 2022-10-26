# 서울에 전기차 충전소는 어디에 몇개가 필요해질까?
- 26년까지 전기차를 40만대까지 늘린다고 하는데
- 전기차 충전소 22만대를 보급한다고 했는데 충분한가
- 그러면 전기차 충전소는 어디에 얼마나 필요해질까?

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import requests
import json
import plotly.express as px

# 지수표현식 제거하기
pd.options.display.float_format = '{:.5f}'.format

import koreanize_matplotlib
# 그래프에 retina display 적용
%config InlineBackend.figure_format = 'retina'

## 서울시 전기차

file_name = ("data/서울특별시 친환경자동차 현황.CSV")
raw = pd.read_csv(file_name, encoding='cp949')

raw = raw.loc[raw['연료'] == '전기', ['기준년월', '사용본거지시읍면동_행정동기준', '차명', '연료']]
raw = raw.rename(columns={"사용본거지시읍면동_행정동기준":"주소"})
raw = raw.dropna()

raw["구"] = raw["주소"].map(lambda x : x.split()[1])

### 서울시 구별 전기차 수

df = raw.groupby("구")["차명"].count().sort_values(ascending=False).to_frame()
df = df.rename(columns={"차명" : "전기차수"})
df

ev_car_top5 = df.head()#

# 구 별 전기차 TOP 5
explode = [0.1,0.05, 0.05,0.05,0.05]
plt.figure(figsize=(10,10))
plt.pie(ev_car_top5['전기차수'], labels=ev_car_top5.index, explode=explode, autopct='%.d%%')
plt.show()

# 서울시 전기차 수 비율
wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 1}
colors = ['#c1abff', '#d8e1c5', '#80afe5', '#ddadd0', '#ebbfea', '#84cec0', '#9acee9', '#d6c2b6', '#d48c9d', '#dcf6c5']
plt.figure(figsize=(10,10))
plt.pie(df['전기차수'], labels=df.index, autopct='%.d%%', colors = colors,
       shadow=True,
        wedgeprops=wedgeprops)
plt.title("서울시 전기차 수 비율")
plt.show()

### 서울시 총 전기차 수

df["전기차수"].sum()

## 서울시 충전소

ev_raw = pd.read_excel("Data/서울시충전기.xlsx")

ev_raw.head(2)

### 서울시 구별 충전소 갯수

# 시군구로 count 해보기
ev_df = ev_raw.groupby("시군구")["충전소"].count().sort_values(ascending=False).to_frame()
# index 이름을 시군구에서 구로 변경
ev_df.index = ev_df.index.set_names("구")
ev_df

ev_df5 = ev_df.head()

# 구 별 전기차 충전소
explode = [0.1,0.05, 0.05,0.05,0.05]
wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 1}
colors = ['#c1abff', '#d8e1c5', '#80afe5', '#ddadd0', '#ebbfea', '#84cec0', '#9acee9', '#d6c2b6', '#d48c9d', '#dcf6c5']
plt.figure(figsize=(10,10))
plt.pie(ev_df['충전소'], labels=ev_df.index, autopct='%.d%%', colors = colors,
       shadow=True,
        wedgeprops=wedgeprops)
plt.title("구 별 전기차 충전소")
plt.show()

### 서울시 총 충전소 갯수

ev_df["충전소"].sum()

### 두 df 합치기

# index 공백제거
ev_df.index = ev_df.index.str.strip()

df = df.merge(ev_df, left_index=True, right_index=True)
df

### 현재 충전소당 전기차 시각화

df["현재충전소당전기차"] = df["전기차수"] / df["충전소"]

plt.figure(figsize=(20,6))
sns.barplot(data=df, x=df.index, y="현재충전소당전기차", ci=None).set_title("현재충전소당전기차")

- 비율이 잘 안맞는 상태이다
- 이 비율대로 전기차 충전소를 늘리면 큰 불편을 겪을 수도 있다. 

# 미래 서울시 전기차는 총 40만대를 목표로 하고 있다.
- 각 구에 몇대가 늘어나게 될까. 
- 그러면 현재 비율기준으로 전기차 충전소가 얼마나 필요할까.

# 현재 전기차 댓수 / 충전소갯수 / 전기차대충전소비율
df["전기차수"].sum() , df["충전소"].sum(), df["충전소"].sum() / df["전기차수"].sum()

# 필요한 충전소 갯수 
ev_easy_count = round(400000 * (df["충전소"].sum() / df["전기차수"].sum()))
ev_easy_count

#### 서울시의 목표량과 비교

# 서울시의 목표량
seoul_ev = 220000 + df["충전소"].sum()
seoul_ev

# 부족해보이는 갯수
round(400000 * (df["충전소"].sum() / df["전기차수"].sum())) - (220000 + df["충전소"].sum())

## 40만대가 될때 각 구별 전기차 수 예측

# 비율 * 40만대
df["미래전기차수"] = round((df["전기차수"] / df["전기차수"].sum()) * 400000).astype(int)

df

ev_st_top = df['현재충전소당전기차'].sort_values(ascending=False).head(1).to_frame()

ev_st_tail = df['현재충전소당전기차'].sort_values(ascending=False).tail(1).to_frame()

aa = pd.concat([ev_st_top, ev_st_tail])

aa.plot(kind='bar', rot=0, title="충전소 1곳 당 전기차 수용가능 수치 최대-최소 차이 비교", figsize=(10,3))

### 현재 충전소 분포 비율기준으로 미래 충전소 갯수

# 현재 기준 단순 예측
future_station = round((df["충전소"] / df["충전소"].sum()) * ev_easy_count).astype(int)

future_station5 = future_station.head()

explode = [0.1,0.05, 0.05,0.05,0.05]
wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 1}
colors = ['#c1abff', '#d8e1c5', '#80afe5', '#ddadd0', '#ebbfea', '#84cec0', '#9acee9', '#d6c2b6', '#d48c9d', '#dcf6c5']
plt.figure(figsize=(10,10))
plt.pie(ev_df['충전소'], labels=ev_df.index, autopct='%.d%%', colors = colors,
       shadow=True,
        wedgeprops=wedgeprops)
plt.title("미래 구 별 전기차 충전소 설치 개수 가정")
plt.show()

# 충전소 확충시 기존 주유소 분포를 참고하는게 좋은까 인구분포로 참고하는게 좋을까?

1주유소는 기존 자동차 수에 대해 충분히 분포하고 있다고 가정한다.


2 전기차는 인구밀도에도 영향이 있을 수 있다. 

---
- 주유소와 인구비 확인하기
- 전기차충전소와 인구비 확인하기

## 서울시 총 인구 데이터
- 2021년 기준

people = pd.read_csv("data/서울시인구데이터2021.csv", encoding="cp949")
people.head(3)

# 전처리
people = people[["행정구역별(읍면동)", "2021"]].iloc[2:]
people = people.reset_index(drop=True)
people = people.rename(columns={"행정구역별(읍면동)":"구","2021":"인구"})
people = people.set_index("구")
people

# 숫자타입으로변경
people["인구"] = people["인구"].astype(int)

plt.figure(figsize=(20,6))
sns.barplot(data=people, x=people.index, y="인구", ci=None).set_title("인구")

## 서울시 주유소 데이터

oil = pd.read_csv("data/서울시주유소.csv", encoding="cp949")
oil.head()

oil_df = oil.groupby("자치구명")[["주유소명"]].count()

oil_df.index = oil_df.index.set_names("구")

oil_df = oil_df.rename(columns={"주유소명":"주유소 수"})

### 서울시 구별 주유소 갯수

oil_df

### 인구와 주유소데이터 합치기

df_op = people.merge(oil_df, left_index=True, right_index=True)
df_op

### 전기차 데이터와 합치기

df = df_op.merge(df, left_index=True, right_index=True)
df

df.corr()

plt.figure(figsize=(15, 10))
sns.heatmap(df.corr(), cmap="Greens", annot=True)

# 중간인사이트
- 주유소와 충전소의 갯수가 인구보다 더 상관관계에 있다. 
- 인구에 비례하게 하기보다는, 주유소의 비율로 충전소를 늘리는게 더 유의미하다고 생각했다. 
- 휘발유차 대비 얼만큼의 주유소가 있는지 확인해보자

## 서울시 휘발유 자동차 데이터

car_raw = pd.read_csv("data/서울시자동차등록수.csv", encoding="cp949")
car_raw = car_raw[4:]

car_raw["구"] =  car_raw["행정동-연료별 분류"].map(lambda x : x.split()[1].strip())

car_df = car_raw[["구","경유","하이브리드(경유-전기)","하이브리드(휘발유-전기)","휘발유","휘발유(무연)","휘발유(유연)"]]
car_df

# 결측치 확인
car_df.isnull().sum()

# 결측치를 0으로 변경
car_df = car_df.fillna(0)

# 구별로 묶어주기
car_df = car_df.groupby("구").sum()

car_df["휘발유자동차수"] = car_df.sum(axis=1).astype(int)

car_df

### 구별 휘발유 자동차 수

car_df = car_df[["휘발유자동차수"]]
car_df

### df 와 합치기

df = df.merge(car_df, left_index=True, right_index=True)
df

### 주유소당 휘발유자동차 수  

df["주유소당자동차"] = df["휘발유자동차수"] / df["주유소갯수"]

### 자동차당 주유소

df["자동차당주유소비율"] = df["주유소갯수"] / df["휘발유자동차수"] * 100

df

## 자동차당주유소 비율에 맞게 전기차 충전소를 배치해보자

# 서울시가 목표로 하는 충전소갯수
seoul_ev

# 자동차당주유소비율로 전기차 충전소 갯수 추천
(df["자동차당주유소비율"] * df["미래전기차수"] * 37).sum()

df["주유소비율로본미래충전소갯수"] = (df["자동차당주유소비율"] * df["미래전기차수"] * 37)

plt.figure(figsize=(20,6))
sns.barplot(data=df, x=df.index, y="주유소비율로본미래충전소개수", ci=None).set_title("주유소비율로본미래충전소개수")

df["미래충전소당전기차예측(주유소기준)"] = df["미래전기차수"] / df["주유소비율로본미래충전소갯수"]
df["미래충전소당전기차예측(주유소기준)"].to_frame()

plt.figure(figsize=(20,6))
sns.barplot(data=df, x=df.index, y="미래충전소당전기차예측(주유소기준)", ci=None).set_title("미래충전소당전기차예측(주유소기준)")

### 만약 인구비로 충전소를 늘린다면?
- 인구가 많은 쪽에 충전소를 늘려야 한다고 접근하면 어떻게 될까?


df["인구비"] = df["인구"] / df["인구"].sum()

seoul_ev

(df["인구비"] * df["미래전기차수"] * 13.7).sum()

df["인구비율로본미래충전소개수"] = (df["인구비"] * df["미래전기차수"] * 13.7)

plt.figure(figsize=(20,6))
sns.barplot(data=df, x=df.index, y="인구비율로본미래충전소개수", ci=None).set_title("인구비율로본미래충전소개수")

df["미래충전소당전기차예측(인구기준)"] = df["미래전기차수"] / df["인구비율로본미래충전소갯수"]

plt.figure(figsize=(20,6))
sns.barplot(data=df, x=df.index, y="미래충전소당전기차예측(인구기준)", ci=None).set_title("미래충전소당전기차예측(인구기준)")

- 인구비로 늘렸을때는, 종로구, 중구 등에서 전기차 예상수요를 따라가지 못하는걸로 보인다. 

# 지도 시각화

# 서울 행정구역 json raw파일(githubcontent)
r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
c = r.content
seoul_geo = json.loads(c)

# 위도
lat = 37.394946
# 경도
lon = 127.111104

# 서울시 전기차 대수
m1 = folium.Map(
    location=[lat, lon],
    zoom_start=11, 
    tiles='cartodbpositron'
)


folium.GeoJson(
    seoul_geo,
    name='지역구'
).add_to(m1)

m1.choropleth(geo_data=seoul_geo,
             data=df['전기차수'], 
             fill_color='YlGnBu', # 색상 변경도 가능하다
             fill_opacity=0.5,
             line_opacity=0.2,
             key_on='properties.name',
             legend_name="행정동별 전기차 수"
            )
m1

# 서울시 충전소 개수
m2 = folium.Map(
    location=[lat, lon],
    zoom_start=11, 
    tiles='cartodbpositron'
)

folium.GeoJson(
    seoul_geo,
    name='지역구'
).add_to(m2)

m2.choropleth(geo_data=seoul_geo,
             data=df['충전소'], 
             fill_color='YlGnBu', # 색상 변경도 가능하다
             fill_opacity=0.5,
             line_opacity=0.2,
             key_on='properties.name',
             legend_name="행정동별 충전소 개수"
            )
m2

px.bar(df[['미래전기차수', "휘발유자동차수", "전기차수"]], barmode='group',width=1000,
    height=500)
