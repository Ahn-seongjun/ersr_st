
import streamlit as st
import pandas as pd
import plotly.express as px
import os, base64


# 수입
ersr_over = pd.read_csv('./data/해외말소1507_2406.csv')
ersr_over['EXTRACT_DE'] = ersr_over['EXTRACT_DE'].astype('str')
ersr_over['EXTRACT_DE'] = pd.to_datetime(ersr_over['EXTRACT_DE'])
ersr_over['MAX_AVG_TRVL'] = round(ersr_over['TRVL'] * ersr_over['USE_YEAR'], -3)
trvl_over = ersr_over.pivot(index='EXTRACT_DE', columns='ORG_CAR_MAKER_KOR', values='MAX_AVG_TRVL')
trvl_over = trvl_over.reset_index()
trvl_over.dropna(axis=1, inplace=True)
# 국산
ersr_na = pd.read_csv('./data/국내말소1507_2406.csv')
ersr_na['EXTRACT_DE'] = ersr_na['EXTRACT_DE'].astype('str')
ersr_na['EXTRACT_DE'] = pd.to_datetime(ersr_na['EXTRACT_DE'])
ersr_na['MAX_AVG_TRVL'] = round(ersr_na['TRVL'] * ersr_na['USE_YEAR'], -3)
trvl_na = ersr_na.pivot(index='EXTRACT_DE', columns='ORG_CAR_MAKER_KOR', values='MAX_AVG_TRVL')
trvl_na = trvl_na.reset_index()
trvl_na.dropna(axis=1, inplace=True)
#trvl_na.columns[1:].tolist()
def st_button(url, label):
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)
    button_code = f'''<a href="{url}" target=_blank 
    style = background-color: white;
        border-color : #ffffff;
        border-style:double;
        text-align: center;> {label}</a>'''

    return st.markdown(button_code, unsafe_allow_html=True)


st.set_page_config(page_title= "summary", layout="wide", initial_sidebar_state="auto")







with st.sidebar:
    st.write("CARISYOU DATALAB")

    CC = st.button("임시 비활성화입니다.")
    #if CC:
        #webbrowser.open_new_tab("https://carcharts-free.carisyou.net/?utm_source=Carisyou&utm_medium=Banner&utm_campaign=P03_PC_Free&")
        #webbrowser.open("https://carcharts-free.carisyou.net/?utm_source=Carisyou&utm_medium=Banner&utm_campaign=P03_PC_Free&", new=0, autoraise=True)

st.markdown("## 말소 주행거리 분석 이동평균 자료")
st.markdown(f"- 데이터 값 산출 근거 : 월별, 브랜드별 평균 주행거리 X 평균 사용년수")
st.markdown("#### 이동평균 그래프 사용 방법")
st.markdown(f"- 차수 기준으로 이동평균선 조정 가능합니다.")
st.markdown(f"- 국산/수입 탭을 통해 국산, 수입 변경 가능합니다.")
st.markdown(f"- 하단의 브랜드 콤보박스를 통해 브랜드 설정 가능합니다.")

number = st.number_input('MA 차수', 1, 36)

tab1, tab2 = st.tabs(['국산','수입'])
with tab1:
    st.subheader('국산차량 말소 주행거리 이동평균선')
    brand1 = st.selectbox("브랜드", trvl_na.columns[1:].tolist())

    ma_fig_na = px.scatter(trvl_na, x="EXTRACT_DE", y=brand1, trendline="rolling",
                           trendline_options=dict(window=number),
                           title=f"{number}-point moving average")
    st.plotly_chart(ma_fig_na, use_container_width=True)

with tab2:
    st.subheader('수입차량 말소 주행거리 이동평균선')
    brand = st.selectbox("브랜드", trvl_over.columns[1:].tolist())
    ma_fig_over = px.scatter(trvl_over, x="EXTRACT_DE", y=brand, trendline="rolling", trendline_options=dict(window=number),
                     title=f"{number}-point moving average")
    st.plotly_chart(ma_fig_over, use_container_width=True)


with open('./assets/carcharts.png', "rb") as f:
    data = f.read()


footer=f"""<style>
.footer {{
position: fixed;
left: 0;
bottom: 0;
width: 100%;
height : 30px;
background-color: white;
color: black;
border-width : 5px;
border-color : gray white white white;
border-style:double none none none;
text-align: center;

}}
</style>

<div class="footer">
<center> Copyright &copy; All rights reserved |  <a href="https://carcharts.carisyou.net/" target=_blank><img src="data:image/png;base64,{base64.b64encode(data).decode()}" class='img-fluid' style = "width:75px; height:25px;"> </center>
</div>

"""


st.markdown(footer,unsafe_allow_html=True)

# import pandas as pd
# df = pd.read_csv('C:/Users/clmns/PycharmProjects/pythonProject1/carregdb/data/2023년 누적 데이터.csv', index_col=0)
# df5 = df[(df['EXTRACT_DE'] == 20231201) & (df['CL_HMMD_IMP_SE_NM'] == '국산')]
# print(df5)

# streamlit run summary.py