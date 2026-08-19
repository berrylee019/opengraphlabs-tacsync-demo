 Physical AI Data Pipeline & Tactile Sync Monitor (PoC)

> [Open Graph Labs 협업 제안용 PoC 프로젝트]
> 멀티모달 센서 데이터의 밀리초(ms) 단위 동기화 정합성 검증 및 AI 학습용 데이터 품질(QA) 시뮬레이션 대시보드

🔗 Live Demo: [ogl-tactile-sync.streamlit.app]

---

##  Project Background & Intent
오픈그래프랩스(Open Graph Labs)가 주력하는 **'Tactile-grounded annotation'** 및 **'Synchronize any hardware'** 기술 스택에서 영감을 받아 제작한 실무형 프로토타입(PoC)입니다. 

방대한 제조/서비스 현장의 멀티모달(비전·촉각·관절 로그) 데이터를 수집·가공하는 과정에서 발생하는 **동기화 병목(Drift)**과 **데이터 정합성 검증**을 웹 환경에서 직관적으로 해결할 수 있는 시각화 유틸리티를 목표로 합니다.

---

##  Key Features (핵심 기능)

1. **Multi-Modal Time-Series & Sync Alignment**
   - 비전 프레임 타임스탬프와 촉각 압력(Tactile Pressure), 로봇 관절 로그 간의 밀리초(ms) 단위 동기화 파형 시각화 (`Plotly`)
2. **Tactile-Grounded Heatmap Simulator**
   - 로봇 파지(Grasping) 순간의 표면 압력 분포를 타임라인 스크러버와 연동하여 실시간 히트맵으로 구현
3. **Automated Quality Assurance (QA) Log Stream**
   - 설정된 동기화 오차(Drift) 임계값을 기반으로 AI 학습에 최적화된 데이터 구간을 자동으로 필터링 및 경고 처리

---

##  Tech Stack
* **Language:** Python 3.9+
* **Framework:** Streamlit
* **Visualization:** Plotly, Pandas, NumPy

---

##  Run Locally (로컬 실행 방법)

저장소를 클론한 후, 아래 명령어로 즉시 실행해 볼 수 있습니다.

```bash
# 1. 저장소 클론
git clone [https://github.com/berrylee019/opengraphlabs-tacsync-demo.git](https://github.com/berrylee019/opengraphlabs-tacsync-demo.git)
cd opengraphlabs-tacsync-demo

# 2. 패키지 설치
pip install -r requirements.txt

# 3. Streamlit 앱 실행
streamlit run app.py
