import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 테마 설정 (학술적인 느낌을 위해 Wide 모드 유지)
st.set_page_config(page_title="Education Investment Analysis", layout="wide")

# 학술적인 분위기를 위한 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stHeading h1 { color: #1e3a8a; font-family: 'Times New Roman', serif; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 상단 헤더 (논문 형식) ---
st.title("🎓 국가별 소득 수준에 따른 교육 지출의 구조적 상관관계 분석")
st.markdown("""
**연구 배경:** 본 대시보드는 세계은행(World Bank)의 데이터를 바탕으로 국가의 경제적 수준(GDP)과 
교육 단계별(초등·중등·고등) 지출 비중 간의 통계적 유의성을 탐색합니다.
---
""")

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    # 실제 데이터 구조를 반영한 샘플
    data = {
        'Country': ['South Korea', 'USA', 'Finland', 'Norway', 'Germany', 'Japan', 'Vietnam', 'Brazil', 'Ethiopia', 'India'],
        'Income_Group': ['High income', 'High income', 'High income', 'High income', 'High income', 'High income', 'Lower middle income', 'Upper middle income', 'Low income', 'Lower middle income'],
        'Total_Exp_GDP': [5.1, 4.9, 6.3, 7.5, 4.8, 3.2, 4.1, 6.0, 4.5, 3.8],
        'Primary': [35, 30, 25, 20, 28, 32, 40, 30, 50, 45],
        'Secondary': [35, 35, 40, 45, 42, 38, 35, 40, 30, 35],
        'Tertiary': [30, 35, 35, 35, 30, 30, 25, 30, 20, 20],
        'Years_of_Data': [50, 45, 48, 55, 52, 50, 20, 35, 15, 30]
    }
    return pd.DataFrame(data)

df = load_data()

# --- 사이드바: 데이터 컨트롤 및 방법론 ---
with st.sidebar:
    st.header("⚙️ 분석 설정")
    uploaded_file = st.file_uploader("추가 데이터셋 업로드 (.csv)", type="csv")
    if uploaded_file:
        df = pd.concat([df, pd.read_csv(uploaded_file)], ignore_index=True)
    
    st.markdown("---")
    st.markdown("### 📖 분석 방법론")
    st.caption("본 분석은 GDP 대비 교육비 지출 총액을 독립 변수로, 교육 단계별 비중을 종속 변수로 설정하여 분석합니다.")
    st.latex(r"E_{total} = \sum_{i \in \{p, s, t\}} e_i")

# --- 본문 1: 기술 통계 요약 ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("분석 대상 국가 수", f"{len(df)}개국")
with col2:
    st.metric("평균 교육 지출 (GDP %)", f"{df['Total_Exp_GDP'].mean():.2f}%")
with col3:
    st.metric("최장 데이터 보유", f"{df['Years_of_Data'].max()}년")

# --- 본문 2: 인터렉티브 분석 차트 ---
st.subheader("🔍 1. 소득 수준별 지출 분포 (Statistical Distribution)")

# Plotly 테마를 'plotly_white'로 설정하여 학술지 느낌 강조
fig1 = px.box(df, x='Income_Group', y='Total_Exp_GDP', 
             color='Income_Group', points="all", notched=True,
             color_discrete_sequence=px.colors.qualitative.Slate)
fig1.update_layout(template="plotly_white", showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- 본문 3: 교육 단계별 포트폴리오 ---
st.subheader("📚 2. 교육 단계별 투자 포트폴리오 분석")
tab1, tab2 = st.tabs(["상위 10개국 비교", "전체 국가 상관관계"])

with tab1:
    top10 = df.nlargest(10, 'Total_Exp_GDP')
    fig2 = go.Figure()
    for stage in ['Primary', 'Secondary', 'Tertiary']:
        fig2.add_trace(go.Bar(name=stage, x=top10['Country'], y=top10[stage]))
    fig2.update_layout(barmode='stack', template="plotly_white", yaxis_title="지출 비중 (%)")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # 학술적인 느낌의 Ternary Plot 추가
    fig3 = px.scatter_ternary(df, a="Primary", b="Secondary", c="Tertiary",
                             color="Income_Group", size="Total_Exp_GDP",
                             hover_name="Country", template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)
    st.info("💡 점이 상단에 가까울수록 초등교육, 좌측은 중등, 우측은 고등교육 비중이 높음을 의미합니다.")

# --- 본문 4: 데이터 테이블 및 연구 주석 ---
with st.expander("📝 Raw Data 및 연구 주석 확인"):
    st.table(df.sort_values('Total_Exp_GDP', ascending=False))
    st.markdown("""
    **Data Source:** World Bank Education Statistics.  
    **Note:** 일부 국가의 데이터는 보고 연도에 따라 편차가 있을 수 있습니다.
    """)
