import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# app.py에 추가할 코드 조각
st.sidebar.subheader(" Quick Test Data")
if st.sidebar.button("Load Sample CSV"):
    uploaded_file = "sample.csv"

st.set_page_config(page_title="Tactile Sync Engine", layout="wide")

st.title("🛡️ Tactile Sync Engine: Multi-Modal Log Parser")
st.markdown("실제 센서 로그(CSV)를 업로드하면 타임라인 정합성을 즉시 분석합니다.")

# 1. 파일 업로드 섹션
uploaded_file = st.sidebar.file_uploader("Upload Sensor Log (CSV)", type=["csv"])

if uploaded_file is not None:
    # CSV 파싱
    df = pd.read_csv(uploaded_file)
    
    # 필수 컬럼 검사 (오픈그래프랩스 스타일의 멀티모달 로그 가정)
    required_cols = ['Timestamp', 'Tactile_Pressure_Left', 'Tactile_Pressure_Right', 'Joint_Angle_Pitch']
    if all(col in df.columns for col in required_cols):
        
        # 2. 대시보드 시각화 로직
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Data Overview")
            st.write(df.head())
            
        with col2:
            st.subheader("Sync Drift Analysis")
            # 가상 동기화 오차 계산 (실제 데이터에선 로직 추가 가능)
            st.line_chart(df[['Timestamp', 'Tactile_Pressure_Left', 'Tactile_Pressure_Right']])

        # 3. 실시간 인터랙션 시각화
        st.subheader("Tactile-Grounded Heatmap")
        time_select = st.slider("Select Time", float(df['Timestamp'].min()), float(df['Timestamp'].max()))
        
        # 선택한 시간대의 데이터 필터링
        current_data = df.iloc[(df['Timestamp'] - time_select).abs().argsort()[:1]]
        val_l = current_data['Tactile_Pressure_Left'].values[0]
        
        # 히트맵 시뮬레이션
        heatmap_data = np.random.rand(5,5) * (val_l / 50)
        fig_heat = px.imshow(heatmap_data, color_continuous_scale="Reds")
        st.plotly_chart(fig_heat, use_container_width=True)

    else:
        st.error(f"데이터 형식이 맞지 않습니다. 필수 컬럼: {required_cols}")
else:
    st.info("시뮬레이션을 위해 샘플 로그를 업로드해주세요.")
    # 샘플 데이터 다운로드 링크 제공
    sample_df = pd.DataFrame({
        'Timestamp': np.arange(0, 5, 0.1),
        'Tactile_Pressure_Left': np.random.rand(50) * 100,
        'Tactile_Pressure_Right': np.random.rand(50) * 100,
        'Joint_Angle_Pitch': np.random.rand(50) * 90
    })
    st.download_button("샘플 데이터 받기", sample_df.to_csv(index=False), "sample_log.csv")
