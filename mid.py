import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px
import folium
import requests
import json

file_name = ("final_data.csv")
df = pd.read_csv(file_name, encoding='cp949')

st.set_page_config(
    page_title="전기차와 충전소 분석",
    page_icon="🚗",
    layout="wide",
)

st.markdown("# 전기차 분석🚗")
st.sidebar.markdown("# 전기차 분석🚗")

st.header("인구")
ptx = px.bar(df, y="인구", x="구", width=1200, height=700)
ptx

st.header('전기차 수')
pxh = px.histogram(df, x="구", y="전기차수", color = '전기차수', width=1200, height=700)
pxh

st.markdown("## 전기차수")
st.line_chart(data=df, x="구", y="전기차수", width=1200, height=700)

st.markdown("## 인구-휘발유자동차수-전기차수")
ptx = px.line(df,  x="구", y=["인구", "휘발유자동차수", "전기차수"], width=1200, height=700)
ptx
ptx = px.bar(df,  x="구", y=["인구", "휘발유자동차수", "전기차수"], width=1200, height=700)
ptx

st.markdown("## 휘발유자동차수-전기차수")
ptx = px.line(df,  x="구" , y=["휘발유자동차수", "전기차수"], width=1200, height=700)
ptx

st.markdown("## 휘발유 자동차 비율")
pie = px.pie(df, values='휘발유자동차수', names='구', width=1200, height=700)
st.plotly_chart(pie)

st.markdown("## 전기차 자동차 비율")
pie = px.pie(df, values='전기차수', names='구', width=1200, height=700)
st.plotly_chart(pie)

st.markdown("## 상관계수")
fig, ax = plt.subplots(figsize=(10, 3))
mask = np.triu(np.ones_like(df[["인구", "주유소개수", "전기차수", "충전소개수", "휘발유자동차수"]].corr()))
sns.heatmap(df[["인구", "주유소개수", "전기차수", "충전소개수", "휘발유자동차수"]].corr(), annot=True, fmt=".2f", cmap="Greens", mask=mask)
st.pyplot(fig)


df_l = df[['longitude', 'latitude']]

map_data = pd.DataFrame(
    np.random.randn(25, 2) / [50, 50] + df_l,
    columns=['longitude', 'latitude'])
st.map(map_data)

st.header("서울시 구별 전기차 수")
ev_num_df = df[["구", "전기차수"]].sort_values("구").set_index("구")
st.dataframe(ev_num_df)
fig, ax = plt.subplots(figsize=(17,9))
my_colours = ['#c1abff', '#d8e1c5', '#80afe5', '#ddadd0', '#ebbfea', '#84cec0', '#9acee9', '#d6c2b6', '#d48c9d', '#dcf6c5']
wed={"width": 0.4}
explode = [0.1,0.05, 0.05,0.05,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pie = ax.pie(df["전기차수"],labels=ev_num_df.index,
            colors=my_colours,explode=explode,
            wedgeprops=wed,shadow=True)
st.pyplot(fig)

file_n = ("seoul.csv")
place = pd.read_csv(file_name, encoding='cp949')
place_l = place[['longitude', 'latitude']]
map_dt = pd.DataFrame(
    np.random.randn(25, 2) / [50, 50] + place_l,
    columns=['longitude', 'latitude'])
st.map(map_dt)
