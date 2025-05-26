import streamlit as st
import pandas as pd

st.set_page_config(page_title="다문화 학생수 변화 시각화", layout="wide")
st.title("연도별·학제별·국적별 다문화 학생수 변화")

# 1. 업로드된 엑셀 파일을 바로 로드
DATA_PATH = "data.xlsx"
try:
    df = pd.read_excel(DATA_PATH)
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 컬럼명 확인 및 표준화
df.columns = df.columns.str.strip()
# 필수 컬럼 체크
required_cols = ['연도', '학제', '국가', '학생수']
if not all(col in df.columns for col in required_cols):
    st.error(f"데이터에 필요한 컬럼이 없습니다. 최소한 {', '.join(required_cols)} 컬럼이 포함되어야 합니다.")
    st.stop()

# 사이드바 필터
st.sidebar.header("필터 설정")
levels = df['학제'].unique().tolist()
selected_level = st.sidebar.selectbox("학제 선택", levels)

countries = df['국가'].unique().tolist()
selected_countries = st.sidebar.multiselect(
    "국가 선택 (여러 개 선택 가능)", countries, default=countries[:1]
)

# 데이터 필터링 (2012~2024)
filtered = df[
    (df['학제'] == selected_level) &
    (df['국가'].isin(selected_countries)) &
    (df['연도'].between(2012, 2024))
]

if filtered.empty:
    st.warning("선택하신 조건에 맞는 데이터가 없습니다.")
else:
    # 피벗 테이블 생성
    pivot = filtered.pivot_table(
        index='연도', columns='국가', values='학생수'
    ).sort_index()

    # 꺾은선 그래프 출력
    st.subheader(f"[{selected_level}] 학제 - {', '.join(selected_countries)} 국가별 학생수 (2012-2024)")
    st.line_chart(pivot)
