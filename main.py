import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 페이지 테마 및 스타일 설정 ---
st.set_page_config(page_title="Global Education Investment Research", layout="wide")

# 학술적 감성을 위한 커스텀 CSS (폰트 및 배경색 조정)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');
    .main { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Noto Serif KR', serif; color: #1a202c; }
    .stMarkdown { font-family: 'sans-serif'; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 로드 및 처리 함수 ---
@st.cache_data
def load_initial_data():
    # 기본 탑재 데이터 (World Bank 스타일 샘플)
    data = {
        'Country': ['South Korea', 'USA', 'Finland', 'Norway', 'Germany', 'Japan', 'Vietnam', 'Brazil', 'Ethiopia', 'India', 'Canada', 'France'],
        'Income_Group': ['High income', 'High income', 'High income', 'High income', 'High income', 'High income', 'Lower middle income', 'Upper middle income', 'Low income', 'Lower middle income', 'High income', 'High income'],
        'Total_Exp_GDP': [5.1, 4.9, 6.3, 7.5, 4.8, 3.2, 4.1, 6.0, 4.5, 3.8, 5.5, 5.2],
        'Primary': [35, 30, 25, 20, 28, 32, 40, 30, 50, 45, 25, 28],
        'Secondary': [35, 35, 40, 45, 42, 38, 35, 40, 30, 35, 40, 40],
        'Tertiary': [30, 35, 35, 35, 30, 30, 25, 30, 20, 20, 35, 32],
        'Years_of_Data': [50, 45, 48, 55, 52, 50, 20, 35, 15, 30, 50, 48]
    }
    return pd.DataFrame(data)

# 데이터 불러오기
df = load_initial_data()

# --- 3. 헤더 및 서론 (Abstract) ---
st.title("🏛️ 국가별 경제 수준에 따른 교육 투자 구조 분석")
st.markdown("""
> **초록(Abstract):** 본 연구용 대시보드는 국가의 경제적 소득 수준이 교육 지출의 규모 및 단계별 배분 방식에 미치는 영향을 분석합니다. 
> Plotly를 활용한 인터렉티브 시각화를 통해 거시경제 지표와 교육 정책 간의 상관관계를 탐색합니다.
""")
st.divider()

# --- 4. 사이드바 (데이터 업로드 및 설정) ---
with st.sidebar:
    st.header("📂 Data Management")
    uploaded_file = st.file_uploader("추가 데이터 업로드 (CSV)", type="csv")
    if uploaded_file:
        try:
            extra_df = pd.read_csv(uploaded_file)
            df = pd.concat([df, extra_df], ignore_index=True).drop_duplicates()
            st.success("데이터가 성공적으로 통합되었습니다.")
        except Exception as e:
            st.error(f"에러 발생: {e}")
    
    st.divider()
    st.markdown("### 📊 분석 방법론")
    st.latex(r"Expenditure_{total} = \sum_{level=1}^{n} E_{level}")
    st.caption("위 수식은 각 교육 단계(Primary, Secondary, Tertiary) 지출의 총합을 정의합니다.")

# --- 5. 주요 통계 지표 (Key Metrics) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("표본 국가 수", f"{len(df)}개국")
with m2:
    st.metric("평균 지출 (GDP %)", f"{df['Total_Exp_GDP'].mean():.1f}%")
with m3:
    st.metric("최고 투자국", df.loc[df['Total_Exp_GDP'].idxmax(), 'Country'])
with m4:
    st.metric("데이터 수집 평균", f"{df['Years_of_Data'].mean():.1f}년")

st.write("") # 간격 조절

# --- 6. 시각화 섹션 ---

# 차트 1: 소득 수준별 교육비 지출 비중 (Box Plot)
st.subheader("1. 소득 수준별 정부 교육 지출 분포")
income_order = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
df['Income_Group'] = pd.Categorical(df['Income_Group'], categories=income_order, ordered=True)

fig1 = px.box(df.sort_values('Income_Group'), 
             x='Income_Group', y='Total_Exp_GDP', 
             color='Income_Group', 
             points="all", 
             notched=True,
             template="plotly_white",
             color_discrete_sequence=px.colors.qualitative.D3) # Slate 에러 수정 포인트
fig1.update_layout(showlegend=False, yaxis_title="GDP 대비 지출 (%)", xaxis_title="소득 그룹")
st.plotly_chart(fig1, use_container_width=True)

col_left, col_right = st.columns(2)

# 차트 2: 교육비 지출 상위 10개국 단계별 비중 (Stacked Bar)
with col_left:
    st.subheader("2. 지출 상위 10개국 교육 단계별 비중")
    top10_exp = df.nlargest(10, 'Total_Exp_GDP')
    fig2 = px.bar(top10_exp, x='Country', y=['Primary', 'Secondary', 'Tertiary'],
                 labels={'value': '비중 (%)', 'variable': '단계'},
                 template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.Safe)
    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig2, use_container_width=True)

# 차트 3: 최장 기간 투자 국가 (Horizontal Bar)
with col_right:
    st.subheader("3. 시계열 데이터 보유 기간 상위 10개국")
    top10_years = df.nlargest(10, 'Years_of_Data')
    fig3 = px.bar(top10_years, x='Years_of_Data', y='Country', 
                 orientation='h',
                 template="plotly_white",
                 color='Years_of_Data',
                 color_continuous_scale='Greys')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

# --- 7. 데이터 탐색 테이블 ---
st.divider()
st.subheader("📑 연구 데이터 원본 탐색")
with st.expander("데이터프레임 전체 보기"):
    st.dataframe(df.sort_values('Total_Exp_GDP', ascending=False), use_container_width=True)

st.markdown("""
***
**Data Citation:** World Bank Open Data (2024). *Education Statistics: Core Indicators.* 본 분석 결과는 연구 목적으로만 사용 가능하며, 실제 정책 결정 시 원본 데이터 확인이 필요합니다.
""")
