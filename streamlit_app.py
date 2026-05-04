import streamlit as st
import pandas as pd

# 1. 앱 설정 (최상단 고정)
st.set_page_config(page_title="Electrode Lab", layout="wide")

# 2. 제목
st.title("🔋 비대칭 소결 전극 저항 구배 시뮬레이터")

# 3. 데이터 로드 (오류 방지를 위해 가장 단순한 구조로 구성)
try:
    data = [
        {"층": "1층 (Front)", "입자크기(um)": 150, "상대저항": 1.0, "역할": "초기 흡착"},
        {"층": "2층 (Middle)", "입자크기(um)": 120, "상대저항": 2.25, "역할": "이행 구간"},
        {"층": "3층 (Rear)", "입자크기(um)": 45, "상대저항": 4.85, "역할": "최종 포집"}
    ]
    df = pd.DataFrame(data)

    # 화면 분할
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 설계 사양")
        st.table(df)

    with col2:
        st.subheader("📊 저항 구배 시각화")
        st.bar_chart(df.set_index("층")["상대저항"])

    st.success("시스템 정상 작동 중입니다.")

except Exception as e:
    st.error(f"오류 발생: {e}")