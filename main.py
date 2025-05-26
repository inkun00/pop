import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="다문화 학생수 변화 시각화", layout="wide")
st.title("연도별·학제별·국적별 다문화 학생수 변화")

# 1. 로컬에 저장된 엑셀 파일 경로
DATA_PATH = "data.xlsx"
try:
    df = pd.read_excel(DATA_PATH, engine="openpyxl")
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 컬럼명 표준화
df.columns = df.columns.str.strip()

# 기본 식별자 컬럼
df_columns = df.columns.tolist()
id_cols = ['연도', '학제']
# '다문화학생수' 등 합계용 컬럼 제외
exclude_cols = id_cols + [col for col in df_columns if '다문화' in col]
value_cols = [col for col in df_columns if col not in exclude_cols]

# 데이터를 긴 형식으로 변환
df_long = df.melt(
    id_vars=id_cols,
    value_vars=value_cols,
    var_name='국가',
    value_name='학생수'
)

# 연도 컬럼을 정수형으로 변환
df_long['연도'] = pd.to_numeric(df_long['연도'], errors='coerce')
df_long = df_long.dropna(subset=['연도'])
df_long['연도'] = df_long['연도'].astype(int)

# 사이드바 필터 설정
st.sidebar.header("필터 설정")
# 학제 리스트 (NaN 제거 후 문자열 변환)
levels = df_long['학제'].dropna().astype(str).unique().tolist()
levels.sort()
selected_level = st.sidebar.selectbox("학제 선택", levels)

# 국가 리스트 (NaN 제거 후 문자열 변환), 최대 10개 선택 가능
countries = df_long['국가'].dropna().astype(str).unique().tolist()
countries.sort()
selected_countries = st.sidebar.multiselect(
    "국가 선택 (최대 10개)", countries, default=countries[:3], max_selections=10
)

# 2012~2024년 사이 데이터 필터링
filtered = df_long[
    (df_long['학제'].astype(str) == selected_level) &
    (df_long['국가'].astype(str).isin(selected_countries)) &
    (df_long['연도'].between(2012, 2024))
]

if filtered.empty:
    st.warning("선택하신 조건에 맞는 데이터가 없습니다.")
else:
    # Plotly로 꺾은선 그래프 생성
    fig = px.line(
        filtered,
        x='연도',
        y='학생수',
        color='국가',
        markers=True,
        title=f"[{selected_level}] 학제 - {', '.join(selected_countries)} 국가별 학생수 (2012-2024)"
    )
    fig.update_layout(xaxis_title="연도", yaxis_title="학생수")
    st.plotly_chart(fig, use_container_width=True)
