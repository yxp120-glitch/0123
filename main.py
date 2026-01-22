import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="Global Education Dashboard", layout="wide")

st.title("🎓 글로벌 교육 지출 데이터 분석 앱")
st.markdown("전 세계 국가별 GDP 대비 교육비 지출 및 교육 수준별 투자 비중을 분석합니다.")

# --- 데이터 준비 (기본 탑재 데이터) ---
@st.cache_data
def load_default_data():
    # 샘플 데이터 생성 (실제 데이터 파일이 있다면 pd.read_csv 사용)
    data = {
        'Country': ['South Korea', 'USA', 'Finland', 'Vietnam', 'Norway', 'Brazil', 'Ethiopia', 'Germany', 'Japan', 'India'],
        'Income_Group': ['High income', 'High income', 'High income', 'Lower middle income', 'High income', 'Upper middle income', 'Low income', 'High income', 'High income', 'Lower middle income'],
        'Total_Exp_GDP': [5.1, 4.9, 6.3, 4.1, 7.5, 6.0, 4.5, 4.8, 3.2, 3.8],
        'Primary': [35, 30, 25, 40, 20, 30, 50, 28, 32, 45],
        'Secondary': [35, 35, 40, 35, 45, 40, 30, 42, 38, 35],
        'Tertiary': [30, 35, 35, 25, 35, 30, 20, 30, 30, 20],
        'Years_of_Data': [50, 45, 48, 20, 55, 35, 15, 52, 50, 30]
    }
    return pd.DataFrame(data)

# 2. 데이터 업로드 및 병합
uploaded_file = st.sidebar.file_uploader("추가 데이터 업로드 (CSV)", type="csv")
df = load_default_data()

if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    df = pd.concat([df, new_data], ignore_index=True)
    st.sidebar.success("데이터가 성공적으로 업데이트되었습니다!")

# --- 시각화 1: 소득 수준별 교육 지출 비중 ---
st.subheader("📊 1. 소득 수준별 정부 교육 지출 비중 (GDP 대비 %)")
income_order = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
df['Income_Group'] = pd.Categorical(df['Income_Group'], categories=income_order, ordered=True)
df_sorted = df.sort_values('Income_Group')

fig1 = px.box(df_sorted, x='Income_Group', y='Total_Exp_GDP', 
             color='Income_Group', points="all",
             labels={'Total_Exp_GDP': '교육 지출 (GDP %)', 'Income_Group': '소득 수준'},
             title="소득 수준이 높아짐에 따른 교육비 지출 분포")
st.plotly_chart(fig1, use_container_width=True)

# --- 시각화 2: 교육 지출 상위 10개국 교육 단계별 비중 ---
st.subheader("📚 2. 교육비 지출 상위 10개국의 단계별(초/중/고) 투자 비중")
top10_exp = df.nlargest(10, 'Total_Exp_GDP')

fig2 = px.bar(top10_exp, x='Country', y=['Primary', 'Secondary', 'Tertiary'],
             title="상위 10개국 교육 단계별 지출 구성 (%)",
             labels={'value': '지출 비중 (%)', 'variable': '교육 단계'},
             barmode='stack')
st.plotly_chart(fig2, use_container_width=True)

# --- 시각화 3: 최장 기간 교육비 투자 국가 TOP 10 ---
st.subheader("⏳ 3. 최장 기간 교육 데이터 보유 국가 TOP 10")
top10_duration = df.nlargest(10, 'Years_of_Data')

fig3 = px.bar(top10_duration, x='Years_of_Data', y='Country', 
             orientation='h', color='Years_of_Data',
             title="데이터 수집 기간(년) 상위 국가",
             labels={'Years_of_Data': '수집 기간 (년)', 'Country': '국가'},
             color_continuous_scale='Viridis')
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

# 데이터 표 출력
if st.checkbox("전체 데이터 보기"):
    st.dataframe(df)
