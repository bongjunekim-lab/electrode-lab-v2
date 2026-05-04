import streamlit as st
import pandas as pd
import io

# 1. 앱 설정 (최상단 필수)
st.set_page_config(page_title="Electrode Lab Simulator", layout="wide")

# 2. 제목 및 설계 정보
st.title("🔋 비대칭 소결 전극 저항 구배 시뮬레이터")
st.info("비대칭 소결 전극의 층별 임피던스 및 순차 배출 안정성을 분석하는 시스템입니다.")

# 3. 김봉준 님의 설계 데이터 반영 (150/120/45um)
layers = [
    {"Layer": "1st (Front)", "Particle_Size_um": 150, "Thickness_mm": 0.450, "Rel_Resistance": 1.0, "Role": "Flash (Initial)"},
    {"Layer": "2nd (Middle)", "Particle_Size_um": 120, "Thickness_mm": 0.502, "Rel_Resistance": 2.25, "Role": "Bridge (Transition)"},
    {"Layer": "3rd (Rear)", "Particle_Size_um": 45, "Thickness_mm": 0.530, "Rel_Resistance": 4.85, "Role": "Concentration (Final)"}
]
df_layers = pd.DataFrame(layers)

# 주요 성능 지표 계산
total_r = df_layers['Rel_Resistance'].sum()
summary_data = {
    "Sequential Stability Index": round(total_r / 3, 2),
    "Expected Capture Capacity (mg)": 128.0,
    "Trap Duration (min)": 106.1,
    "Total Process Time (min)": 285.6
}

# 4. 화면 레이아웃 구성
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 전극 층별 설계 사양")
    st.table(df_layers)
    
    st.subheader("📊 저항 구배 시각화 (Resistance Gradient)")
    # 레이어별 저항 구배를 막대 그래프로 표시
    st.bar_chart(df_layers.set_index('Layer')['Rel_Resistance'])

with col2:
    st.subheader("💡 성능 분석 결과")
    for metric, value in summary_data.items():
        st.metric(label=metric, value=value)

# 5. 설계 보고서 다운로드 기능 (웹 최적화)
st.divider()
st.subheader("📥 설계 보고서 추출")

# 엑셀 파일 생성 (메모리 버퍼 활용)
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_layers.to_excel(writer, sheet_name='Layer_Spec', index=False)
    pd.DataFrame([summary_data]).to_excel(writer, sheet_name='Performance', index=False)

st.download_button(
    label="엑셀 보고서 다운로드 (.xlsx)",
    data=buffer.getvalue(),
    file_name="Electrode_Design_Report.xlsx",
    mime="application/vnd.ms-excel"
)