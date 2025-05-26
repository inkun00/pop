import streamlit as st
import pandas as pd

st.set_page_config(page_title="다문화 학생수 변화 시각화", layout="wide")
st.title("연도별·학제별·국적별 다문화 학생수 변화")

# 1. 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (.xlsx)", type=["xlsx"])
if uploaded_file:
    # 2. 데이터 로드
    df = pd.read_excel(uploaded_file)

    # 컬럼명 확인 및 표준화
    df.columns = df.columns.str.strip()
    # 가정: '연도', '학제', '국가', '학생수' 컬럼이 존재
    if all(col in df.columns for col in ['연도', '학제', '국가', '학생수']):
        st.sidebar.header("필터 설정")
        
        # 1) 학제 선택
        levels = df['학제'].unique().tolist()
        selected_level = st.sidebar.selectbox("학제 선택", levels)

        # 2) 국가 선택 (다중 선택 가능)
        countries = df['국가'].unique().tolist()
        selected_countries = st.sidebar.multiselect(
            "국가 선택 (여러 개 선택 가능)", countries, default=countries[:1]
        )

        # 데이터 필터링
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

            # 3. 꺾은선 그래프 그리기
            st.subheader(f"[{selected_level}] 학제 - {', '.join(selected_countries)} 국가별 학생수 (2012-2024)")
            st.line_chart(pivot)
    else:
        st.error("데이터에 '연도', '학제', '국가', '학생수' 컬럼이 모두 포함되어 있지 않습니다.")
else:
    st.info("우측 또는 상단의 파일 업로더를 통해 엑셀 파일을 업로드해주세요.")
