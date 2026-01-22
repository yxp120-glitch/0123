import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 페이지 테마 및 스타일 설정 ---
st.set_page_config(page_title="Global Education Research", layout="wide")

# 학술적인 서체와 톤앤매너를 위한 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');
    .main { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Noto Serif KR', serif; color: #0f172a; }
    .stMetric { border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 처리 엔진 ---
@st.cache_data
def load_base_data():
    # 학술적 분석을 위한 샘플 데이터셋
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

df = load_base_data()

# 사이드바 설정 (수식 제외)
with st.sidebar:
    st.header("📂 데이터 관리")
    uploaded_file = st.file_uploader("추가 데이터셋 업로드 (CSV)", type="csv")
    if uploaded_file:
        try:
            extra_df = pd.read_csv(uploaded_file)
            df = pd.concat([df, extra_df], ignore_index=True).drop_duplicates()
            st.success("데이터 병합 완료")
        except Exception as e:
            st.error(f"파일 형식 오류: {e}")
    
    st.divider()
    st.markdown("### 📖 분석 방법론")
    st.info("본 대시보드는 국가별 GDP 대비 교육 지출의 총량과 수준별 분배 구조를 비교 분석합니다.")

# --- 3. 메인 대시보드 레이아웃 ---
st.title("🏛️ 글로벌 교육 투자 지표 연구 보고서")
st.markdown("전 세계 국가의 경제적 수준과 교육 단계별 투자 포트폴리오의 상관관계를 시각화합니다.")

# 주요 지표 요약
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("분석 대상 국가", f"{df['Country'].nunique()}개국")
with m2: st.metric("평균 교육 지출", f"{df['Total_Exp_GDP'].mean():.1f}%")
with m3: st.metric("최대 투자국", df.loc[df['Total_Exp_GDP'].idxmax(), 'Country'])
with m4: st.metric("평균 데이터 보유", f"{df['Years_of_Data'].mean():.1f}년")

st.divider()

# --- 4. 시각화 1: 지도 분석 (Choropleth) ---
st.subheader("🌐 1. 지리적 분포: GDP 대비 교육비 지출 규모")
fig_map = px.choropleth(
    df, 
    locations="Country", 
    locationmode='country names',
    color="Total_Exp_GDP", 
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Viridis,
    template="plotly_white"
)
fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)



# --- 5. 시각화 2 & 3: 통계 및 구조 분석 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 2. 소득 수준별 지출 분포")
    income_order = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
    df['Income_Group'] = pd.Categorical(df['Income_Group'], categories=income_order, ordered=True)
    
    fig_box = px.box(
        df.sort_values('Income_Group'), 
        x='Income_Group', 
        y='Total_Exp_GDP', 
        color='Income_Group', 
        points="all", 
        notched=True,
        color_discrete_sequence=px.colors.qualitative.D3,
        template="plotly_white"
    )
    fig_box.update_layout(showlegend=False, yaxis_title="지출 비중 (GDP %)")
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.subheader("📚 3. 지출 상위 10개국 교육 단계별 비중")
    top10_exp = df.nlargest(10, 'Total_Exp_GDP')
    fig_bar = px.bar(
        top10_exp, 
        x='Country', 
        y=['Primary', 'Secondary', 'Tertiary'],
        labels={'value': '비중 (%)', 'variable': '교육 단계'},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_bar.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_bar, use_container_width=True)



# --- 6. 시각화 4: 데이터 지속성 ---
st.subheader("⏳ 4. 최장 기간 교육비 데이터 보유 국가 TOP 10")
top10_years = df.nlargest(10, 'Years_of_Data')
fig_hist = px.bar(
    top10_years, 
    x='Years_of_Data', 
    y='Country', 
    orientation='h', 
    color='Years_of_Data',
    color_continuous_scale='Greys',
    template="plotly_white"
)
fig_hist.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="데이터 수집 기간 (년)")
st.plotly_chart(fig_hist, use_container_width=True)

# --- 7. 데이터 뷰어 ---
st.divider()
with st.expander("📝 연구 데이터 원본 상세 보기"):
    st.dataframe(df.sort_values('Total_Exp_GDP', ascending=False), use_container_width=True)
