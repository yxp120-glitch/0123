import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정 (Flashy UI를 위한 설정)
st.set_page_config(page_title="Data Insights Dashboard", layout="wide", page_icon="📊")

# 커스텀 CSS (UI 개선)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #1f77b4; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f9f9f9; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 로딩 함수 (인코딩 자동 처리 및 캐싱)
@st.cache_data
def load_temp_data(file):
    for enc in ['utf-8', 'cp949', 'euc-kr']:
        try:
            if hasattr(file, 'seek'): file.seek(0)
            df = pd.read_csv(file, encoding=enc, skiprows=7)
            df.columns = df.columns.str.strip()
            df['날짜'] = pd.to_datetime(df['날짜'].str.strip(), errors='coerce')
            df = df.dropna(subset=['날짜', '평균기온(℃)'])
            return df
        except: continue
    return None

# --- 사이드바: 데이터 업로드 ---
st.sidebar.header("📁 데이터 설정")
uploaded_file = st.sidebar.file_uploader("추가 기온 데이터 업로드 (CSV)", type=['csv'])
default_file = 'ta_20260122174530.csv'

if uploaded_file:
    df = load_temp_data(uploaded_file)
    st.sidebar.success("✅ 새로운 데이터 로드 완료")
else:
    try:
        with open(default_file, 'rb') as f:
            df = load_temp_data(f)
        st.sidebar.info("ℹ️ 기본 기온 데이터 로드됨")
    except:
        df = None

# --- 메인 화면 ---
st.title("🚀 데이터 통합 분석 대시보드")

if df is not None:
    tab1, tab2 = st.tabs(["🌡️ 기온 분석 서비스", "🎓 교육 및 경제 지표 (별도 데이터 필요)"])

    with tab1:
        st.header("서울 기온 역사 분석")
        
        # 날짜 선택
        max_date = df['날짜'].max().date()
        min_date = df['날짜'].min().date()
        target_date = st.date_input("비교할 날짜를 선택하세요", value=max_date, min_value=min_date, max_value=max_date)

        # 분석 데이터 추출
        target_month, target_day = target_date.month, target_date.day
        history = df[(df['날짜'].dt.month == target_month) & (df['날짜'].dt.day == target_day)].copy()
        current_data = history[history['날짜'].dt.date == target_date]

        if not current_data.empty:
            curr_temp = current_data['평균기온(℃)'].values[0]
            avg_temp = history['평균기온(℃)'].mean()
            
            # KPI 카드
            c1, c2, c3 = st.columns(3)
            c1.metric(f"{target_date} 기온", f"{curr_temp}℃")
            c2.metric("역대 동일 날짜 평균", f"{avg_temp:.1f}℃", delta=round(curr_temp - avg_temp, 2))
            c3.metric("관측 연수", f"{len(history)}년")

            # 1. 시계열 인터랙티브 차트
            st.subheader(f"📈 역대 {target_month}/{target_day} 기온 변화 추이")
            fig = px.line(history, x=history['날짜'].dt.year, y='평균기온(℃)', 
                         labels={'x':'연도'}, markers=True, title="연도별 기온 변화")
            fig.add_trace(go.Scatter(x=[target_date.year], y=[curr_temp], mode='markers', 
                                     marker=dict(color='red', size=15, symbol='star'), name='선택한 해'))
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

            # 2. 분포 차트
            st.subheader("📊 기온 분포 및 현재 위치")
            fig_hist = px.histogram(history, x="평균기온(℃)", nbins=20, marginal="box", color_discrete_sequence=['#636EFA'])
            fig_hist.add_vline(x=curr_temp, line_dash="dash", line_color="red", annotation_text="선택일 위치")
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("선택한 날짜에 대한 기온 데이터가 없습니다.")

    with tab2:
        st.header("🎓 GDP 및 교육 지출 분석")
        st.info("💡 현재 업로드된 데이터는 '기온' 데이터입니다. 교육 분석을 위해 샘플 레이아웃을 표시합니다.")
        
        # 교육 데이터 샘플 (실제 데이터 업로드 시 이 부분을 df_edu로 교체)
        st.markdown("""
        이 섹션은 **세계은행(World Bank)** 교육 지출 데이터가 있을 때 작동하도록 설계되었습니다.
        기온 데이터에는 해당 컬럼이 없어 현재는 인터페이스 예시를 보여드립니다.
        """)
        
        # 가상 차트 (Plotly 예시)
        dummy_data = pd.DataFrame({
            'Country': ['Korea', 'USA', 'Norway', 'UK', 'Japan', 'Germany', 'France', 'Canada', 'Sweden', 'Israel'],
            'Education_Spending': [4.5, 5.0, 6.7, 5.5, 3.2, 4.8, 5.4, 5.2, 7.1, 6.1],
            'Primary': [1.2, 1.5, 2.1, 1.8, 1.0, 1.4, 1.6, 1.5, 2.2, 1.9],
            'Secondary': [1.8, 2.0, 2.5, 2.2, 1.2, 2.0, 2.2, 2.1, 2.6, 2.5],
            'Tertiary': [1.5, 1.5, 2.1, 1.5, 1.0, 1.4, 1.6, 1.6, 2.3, 1.7]
        }).sort_values('Education_Spending', ascending=False)

        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            st.write("**TOP 10 교육 지출 국가 (GDP 대비 %)**")
            fig_edu = px.bar(dummy_data, x='Country', y='Education_Spending', color='Education_Spending')
            st.plotly_chart(fig_edu, use_container_width=True)
            
        with col_e2:
            st.write("**교육 단계별 지출 비중 (초/중/고)**")
            fig_stack = px.bar(dummy_data, x='Country', y=['Primary', 'Secondary', 'Tertiary'], barmode='stack')
            st.plotly_chart(fig_stack, use_container_width=True)

else:
    st.error("데이터를 불러올 수 없습니다. CSV 파일을 확인해주세요.")
