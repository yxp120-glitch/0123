import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 페이지 설정 및 디자인 ---
st.set_page_config(page_title="Education Investment Global Report", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');
    .main { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Noto Serif KR', serif; color: #1e293b; }
    .stMetric { background-color: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 로드 및 통합 ---
@st.cache_data
def load_data():
    # 기본 데이터셋 (연구용 샘플)
    data = {
        'Country': ['South Korea', 'United States', 'Finland', 'Norway', 'Germany', 'Japan', 'Vietnam', 'Brazil', 'Ethiopia', 'India', 'Canada', 'France', 'Australia', 'South Africa', 'Mexico'],
        'Income_Group': ['High income', 'High income', 'High income', 'High income', 'High income', 'High income', 'Lower middle income', 'Upper middle income', 'Low income', 'Lower middle income', 'High income', 'High income', 'High income', 'Upper middle income', 'Upper middle income'],
        'Total_Exp_GDP': [5.1, 4.9, 6.3, 7.5, 4.8, 3.2, 4.1, 6.0, 4.5, 3.8, 5.5, 5.2, 5.3, 6.2, 4.5],
        'Primary': [35, 30, 25, 20, 28, 32, 40, 30, 50, 45, 25, 28, 30, 35, 38],
        'Secondary': [35, 35, 40, 45, 42, 38, 35, 40, 30, 35, 40, 40, 35, 35, 37],
        'Tertiary': [30, 35, 35, 35, 30, 30, 25, 30, 20, 20, 35, 32, 35, 30, 25],
        'Years_of_Data': [50, 45, 48, 55, 52, 50, 20, 35, 15, 30, 50, 48, 52, 28, 40]
    }
    return pd.DataFrame(data)

df = load_data()

# 사이드바 데이터 업로드
with st.sidebar:
    st.header("📂 데이터 관리")
    uploaded_file = st.file_uploader("추가 데이터셋 업로드 (CSV)", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        df = pd.concat([df, new_df], ignore_index=True).drop_duplicates()
        st.success("데이터 업데이트 완료")
    
    st.divider()
    st.markdown("### 📖 분석 방법론")
    st.info("본 보고서는 세계은행 지표를 기반으로 하며, 국가별 GDP 대비 교육 지출의 지리적/경제적 분포를 다각도로 분석합니다.")

# --- 3. 헤더 및 주요 지표 ---
st.title("🏛️ 글로벌 교육 투자 지표: 지리 및 경제적 구조 분석")
st.markdown("본 연구는 국가별 교육비 지출 데이터를 시각화하여 거시경제적 투자 패턴을 분석하는 데 목적이 있습니다.")

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("분석 대상 국가", f"{df['Country'].nunique()}개국")
with m2: st.metric("평균 교육 지출", f"{df['Total_Exp_GDP'].mean():.2f}%")
with m3: st.metric("평균 데이터 수집 기간", f"{df['Years_of_Data'].mean():.1f}년")
with m4: st.metric("최대 투자 국가", df.loc[df['Total_Exp_GDP'].idxmax(), 'Country'])

st.divider()

# --- 4. 시각화 섹션 1: 지리적 분포 (Choropleth Map) ---
st.subheader("🌐 1. 전 세계 GDP 대비 교육비 지출 지리적 분포")
fig_map = px.choropleth(df, 
                        locations="Country", 
                        locationmode='country names',
                        color="Total_Exp_GDP", 
                        hover_name="Country",
                        color_continuous_scale=px.colors.sequential.Viridis, # 학술적인 Viridis 컬러
                        template="plotly_white")

fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)
[Image of a world choropleth map showing education expenditure as a percentage of GDP by country]

# --- 5. 시각화 섹션 2: 통계적 분석 (Box Plot & Bar Charts) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 2. 소득 수준별 지출 분포")
    income_order = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
    df['Income_Group'] = pd.Categorical(df['Income_Group'], categories=income_order, ordered=True)
    
    fig_box = px.box(df.sort_values('
