import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Physical AI Data Pipeline & Sync Monitor",
    page_icon="🤖",
    layout="wide",
)


# 1. 가상 멀티모달 데이터(Mock Data) 생성 함수
@st.cache_data
def generate_mock_data():
  np.random.seed(42)
  time_steps = np.arange(0, 10.1, 0.1)  # 0초 ~ 10초 (0.1초 간격)

  # 센서 로그 생성
  data = {
      "Timestamp": time_steps,
      "Tactile_Pressure_Left": np.sin(time_steps) * 40
      + 50
      + np.random.normal(0, 2, len(time_steps)),
      "Tactile_Pressure_Right": np.cos(time_steps) * 35
      + 45
      + np.random.normal(0, 2, len(time_steps)),
      "Joint_Angle_Pitch": np.linspace(10, 80, len(time_steps))
      + np.random.normal(0, 1, len(time_steps)),
      "Sync_Drift_ms": np.random.choice([2.1, 3.4, 1.2, 5.0, 2.8], len(time_steps)),
  }
  df = pd.DataFrame(data)
  return df


df = generate_mock_data()

# 2. 상단 타이틀 및 기획 의도 설명
st.title("🛡️ Physical AI Data Pipeline & Tactile Sync Monitor")
st.markdown(
    "**[Open Graph Labs PoC Demo]** — 멀티모달 센서(비전·촉각·관절 로그)의 밀리초(ms) 단위 동기화 정합성 및"
    " AI 학습용 데이터 품질(QA)을 실시간 검증하는 대시보드입니다."
)
st.divider()

# 3. 사이드바 - 제어 패널
st.sidebar.header("🎛️ Pipeline Controls")
selected_hardware = st.sidebar.selectbox(
    "Target Hardware Source",
    [
        "Tactile Glove v2.1",
        "Robotic Arm Array (Any-ROS)",
        "Vision-Tactile Multi-Stream",
    ],
)
qa_threshold = st.sidebar.slider("Drift QA Threshold (ms)", 1.0, 10.0, 4.0)

# 4. 상단 메트릭 요약 (Key Performance Indicators)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Data Source", selected_hardware)
col2.metric("Avg Sync Drift", f"{df['Sync_Drift_ms'].mean():.2f} ms")
col3.metric("Data QA Status", "🟢 PASS (Optimized)", "99.8%")
col4.metric("Total Frames", f"{len(df) * 10} Frames")

st.markdown("")

# 5. 메인 레이아웃: 2분할 (좌측: 실시간 타임라인 및 동기화 / 우측: 촉각 압력 히트맵 시뮬레이션)
main_col1, main_col2 = st.columns([1.2, 0.8])

with main_col1:
  st.subheader("📈 Multi-Modal Time-Series & Sync Alignment")
  st.caption("비전 프레임 타임스탬프와 촉각/관절 센서 로그 간의 정합성 파형")

  # Plotly 인터랙티브 멀티 라인 차트
  fig = go.Figure()
  fig.add_trace(
      go.Scatter(
          x=df["Timestamp"],
          y=df["Tactile_Pressure_Left"],
          name="Left Tactile (kPa)",
          line=dict(color="#FF4B4B", width=2),
      )
  )
  fig.add_trace(
      go.Scatter(
          x=df["Timestamp"],
          y=df["Tactile_Pressure_Right"],
          name="Right Tactile (kPa)",
          line=dict(color="#0068C9", width=2),
      )
  )
  fig.add_trace(
      go.Scatter(
          x=df["Timestamp"],
          y=df["Sync_Drift_ms"] * 10,
          name="Sync Drift (ms x10)",
          line=dict(color="#FFA15A", width=1.5, dash="dot"),
      )
  )

  fig.update_layout(
      xaxis_title="Timeline (Seconds)",
      yaxis_title="Sensor Magnitude",
      height=380,
      margin=dict(l=20, r=20, t=20, b=20),
      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
  )
  st.plotly_chart(fig, use_container_width=True)

with main_col2:
  st.subheader("🖐️ Tactile-Grounded Heatmap")
  st.caption("로봇 파지(Grasping) 순간의 표면 압력 분포 시뮬레이션")

  # 슬라이더로 시간대를 조절하며 가상의 촉각 히트맵 변화 확인
  time_slider = st.slider(
      "Scrub Timeline (sec)",
      min_value=0.0,
      max_value=10.0,
      value=0.0,
      step=0.1,
  )

  # 현재 슬라이더 시간에 따른 가상 5x5 압력 매트릭스 생성
  idx = int(time_slider * 10)
  val_l = df.loc[idx, "Tactile_Pressure_Left"]
  heatmap_data = np.random.uniform(0.1, 0.5, (5, 5)) * val_l / 50
  # 중심부 압력이 높도록 설정
  heatmap_data[2, 2] = val_l / 25

  fig_heat = px.imshow(
      heatmap_data,
      color_continuous_scale="Reds",
      zmin=0,
      zmax=5,
      labels=dict(color="Pressure (kPa)"),
  )
  fig_heat.update_layout(
      height=340, margin=dict(l=20, r=20, t=10, b=10), coloraxis_showscale=True
  )
  st.plotly_chart(fig_heat, use_container_width=True)

# 6. 하단: 자동 QA 및 파이프라인 로그 콘솔
st.divider()
st.subheader("🔍 Automated Quality Assurance (QA) Log Stream")

# Drift 임계값 초과 여부 확인
exceeded_df = df[df["Sync_Drift_ms"] > qa_threshold]

col_log1, col_log2 = st.columns([2, 1])

with col_log1:
  if len(exceeded_df) > 0:
    st.warning(
        f"⚠️ 총 {len(exceeded_df)}개의 구간에서 설정된 임계값({qa_threshold}ms)을"
        " 초과하는 지연(Drift)이 감지되었습니다. (자동 마스킹 대기 중)"
    )
  else:
    st.success(
        "✨ 모든 멀티모달 패킷이 허용 오차 범위 내에서 완벽하게 동기화되었습니다."
    )

with col_log2:
  if st.button("🚀 Run Pipeline QA Optimization", use_container_width=True):
    st.toast("파이프라인 데이터 정제 및 재정렬이 완료되었습니다!", icon="✅")

# 실행 가이드 캡션
st.markdown("---")
st.caption(
    "💡 **Developer Note:** 이 프로토타입은 오픈그래프랩스의 'Synchronize any hardware'와"
    " 'Tactile-grounded annotation' 철학을 웹 환경에서 시각적으로 검증하기 위해 제작되었습니다."
)