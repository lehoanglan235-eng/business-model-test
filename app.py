"""사랑의 언어 성향 테스트 — Streamlit 단일 파일 앱.

실행: pip install streamlit pandas && streamlit run app.py
출처: 사용자가 제공한 'Love Languages Test' PDF의 30문항을 한국어로 번역.
"""

import pandas as pd
import streamlit as st

# A~E는 첨부 PDF의 채점 기준과 동일합니다.
LOVE_LANGUAGES = {
    "A": {
        "name": "인정하는 말",
        "english": "Words of affirmation",
        "emoji": "💌",
        "description": "따뜻한 칭찬, 격려, 감사와 애정 표현을 들을 때 사랑을 크게 느끼는 유형이에요.",
    },
    "B": {
        "name": "함께하는 시간",
        "english": "Quality time",
        "emoji": "🕰️",
        "description": "방해받지 않고 서로에게 집중하며 의미 있는 시간을 보낼 때 가장 깊이 연결돼요.",
    },
    "C": {
        "name": "선물 받기",
        "english": "Receiving gifts",
        "emoji": "🎁",
        "description": "선물의 가격보다 상대가 나를 생각하며 준비한 마음과 정성에서 사랑을 느껴요.",
    },
    "D": {
        "name": "봉사와 도움",
        "english": "Acts of service",
        "emoji": "🤝",
        "description": "집안일을 돕거나 필요한 일을 대신해 주는 등 실제 행동으로 표현한 배려가 중요해요.",
    },
    "E": {
        "name": "스킨십",
        "english": "Physical touch",
        "emoji": "🫂",
        "description": "포옹, 손잡기 등 서로 동의한 다정한 신체 접촉에서 친밀감과 안정감을 느껴요.",
    },
}

# 각 문항은 (선택지 문장, 채점 코드)의 쌍 두 개로 구성됩니다.
# 첨부 PDF 7번의 두 번째 선택지는 'E'로 인쇄되어 있으나
# 내용(인정받는 말)은 A 유형에 해당하므로, 의미에 맞게 A로 채점합니다.
QUESTIONS = [
    [("나를 인정해 주는 짧은 글이나 메시지를 받는 것이 좋다.", "A"), ("포옹을 받는 것이 좋다.", "E")],
    [("가까운 사람과 단둘이 시간을 보내는 것이 좋다.", "B"), ("누군가 실제로 나를 도와줄 때 사랑받는다고 느낀다.", "D")],
    [("다른 사람에게 선물을 받는 것이 좋다.", "C"), ("친구나 사랑하는 사람과 여유롭게 만나는 것이 좋다.", "B")],
    [("다른 사람이 나를 위해 무언가 해 줄 때 사랑받는다고 느낀다.", "D"), ("다른 사람이 나와 신체적으로 접촉할 때 사랑받는다고 느낀다.", "E")],
    [("사랑하거나 존경하는 사람이 내 어깨를 감싸 줄 때 사랑받는다고 느낀다.", "E"), ("사랑하거나 존경하는 사람에게 선물을 받으면 사랑받는다고 느낀다.", "C")],
    [("친구나 사랑하는 사람과 함께 어딘가에 가는 것이 좋다.", "B"), ("소중한 사람과 하이파이브하거나 손을 잡는 것이 좋다.", "E")],
    [("선물처럼 눈에 보이는 사랑의 표현은 내게 매우 중요하다.", "C"), ("다른 사람이 나를 인정해 주는 말을 할 때 사랑받는다고 느낀다.", "A")],
    [("함께 있으면 좋은 사람 곁에 가까이 앉는 것이 좋다.", "E"), ("다른 사람이 나에게 예쁘다거나 멋지다고 말해 주는 것이 좋다.", "A")],
    [("친구나 사랑하는 사람과 시간을 보내는 것이 좋다.", "B"), ("친구나 사랑하는 사람에게 작은 선물을 받는 것이 좋다.", "C")],
    [("있는 그대로의 나를 받아들여 주는 말이 중요하다.", "A"), ("누군가 나를 도와줄 때 그 사람이 나를 사랑한다는 것을 느낀다.", "D")],
    [("친구나 사랑하는 사람과 함께 무언가를 하는 것이 좋다.", "B"), ("다른 사람이 내게 다정한 말을 해 주는 것이 좋다.", "A")],
    [("그 사람이 하는 행동은 말보다 내게 더 큰 영향을 준다.", "D"), ("포옹하면 서로 연결되어 있고 소중히 여겨진다고 느낀다.", "E")],
    [("칭찬을 소중히 여기고 비판은 되도록 피하고 싶다.", "A"), ("큰 선물 하나보다 작은 선물 여러 개가 내게 더 의미 있다.", "C")],
    [("누군가와 이야기하거나 함께 무언가를 할 때 가까워진다고 느낀다.", "B"), ("친구나 사랑하는 사람이 자주 스킨십할 때 더 가까워진다고 느낀다.", "E")],
    [("다른 사람이 내 성취를 칭찬해 주는 것이 좋다.", "A"), ("누군가 내게 도움이 되려고 자신이 좋아하지 않는 일까지 해 줄 때 사랑을 느낀다.", "D")],
    [("친구나 사랑하는 사람이 내 곁을 지나가며 가볍게 스킨십해 주는 것이 좋다.", "E"), ("내 이야기를 진심으로 관심 있게 들어줄 때 좋다.", "B")],
    [("친구나 사랑하는 사람이 내 일이나 프로젝트를 도와줄 때 사랑받는다고 느낀다.", "D"), ("친구나 사랑하는 사람에게 선물 받는 것이 정말 좋다.", "C")],
    [("다른 사람이 내 외모를 칭찬해 주는 것이 좋다.", "A"), ("누군가 내 감정을 이해하려고 시간을 내 줄 때 사랑받는다고 느낀다.", "B")],
    [("소중한 사람이 나와 신체적으로 접촉할 때 안정감을 느낀다.", "E"), ("누군가 나를 위해 도움 되는 행동을 할 때 사랑받는다고 느낀다.", "D")],
    [("소중한 사람들이 나를 위해 해 주는 여러 가지 일에 감사한다.", "D"), ("소중한 사람이 직접 만든 선물을 받는 것이 좋다.", "C")],
    [("누군가 온전히 나에게만 집중해 줄 때 정말 기분이 좋다.", "B"), ("누군가 내 의사결정을 도와줄 때 정말 기분이 좋다.", "D")],
    [("누군가 생일에 선물을 주면 사랑받는다고 느낀다.", "C"), ("누군가 생일에 의미 있는 말로 축하해 주면 사랑받는다고 느낀다.", "A")],
    [("누군가 선물을 주면 그 사람이 나를 생각하고 있었다는 것을 알게 된다.", "C"), ("누군가 내 집안일을 도와줄 때 사랑받는다고 느낀다.", "D")],
    [("누군가 내 말을 끊지 않고 참을성 있게 들어주는 것이 고맙다.", "B"), ("누군가 특별한 날을 기억하고 선물로 챙겨 주는 것이 고맙다.", "C")],
    [("사랑하는 사람이 내 일상적인 일을 도와줄 만큼 나를 신경 쓴다는 사실이 좋다.", "D"), ("소중한 사람과 오랜 시간 여행하는 것이 즐겁다.", "B")],
    [("가까운 사람과 입맞춤을 나누는 것이 좋다.", "E"), ("특별한 이유가 없어도 선물을 받는 것이 좋다.", "C")],
    [("다른 사람에게 고맙고 소중한 존재라는 말을 듣는 것이 좋다.", "A"), ("대화할 때 상대가 나를 바라봐 주는 것이 좋다.", "B")],
    [("친구나 사랑하는 사람이 준 선물은 언제나 특별하다.", "C"), ("친구나 사랑하는 사람이 스킨십해 주면 기분이 좋다.", "E")],
    [("내가 부탁한 일을 누군가 기꺼이 해 줄 때 사랑받는다고 느낀다.", "D"), ("누군가 내게 내가 얼마나 필요한 존재인지 말해 주면 사랑받는다고 느낀다.", "A")],
    [("매일 신체적인 애정 표현이 필요하다.", "E"), ("매일 격려의 말이 필요하다.", "A")],
]

st.set_page_config(page_title="나의 사랑의 언어 💜", page_icon="💜", layout="centered")

# 밝은 보라색 배경과 카드/버튼 스타일 (Streamlit 기본 위젯 사용).
st.markdown("""
<style>
.stApp {background: linear-gradient(160deg, #faf6ff 0%, #f2eaff 60%, #fffaff 100%);}
.block-container {max-width: 790px; padding-top: 2.5rem; padding-bottom: 3rem;}
h1, h2, h3 {color: #603a91 !important;}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.94);
    border: 1px solid #e7d8fa !important;
    border-radius: 22px !important;
    box-shadow: 0 7px 22px rgba(111,70,164,.08);
}
div.stButton > button[kind="primary"] {
    background: #8f62d4; color: white; border: none; border-radius: 12px;
}
div.stButton > button {border-radius: 12px;}
[data-testid="stProgressBar"] div[role="progressbar"] > div {background-color: #9b71dd;}
</style>
""", unsafe_allow_html=True)

# 대화형 앱의 상태: 현재 문항, 응답 저장소, 결과 표시 여부.
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False


def save_answer(question_index: int) -> None:
    """화면의 라디오 버튼 값이 바뀌면 영구 응답 저장소에 복사."""
    selected = st.session_state.get(f"radio_{question_index}")
    if selected is not None:
        st.session_state.answers[question_index] = selected


def restart() -> None:
    """이전 선택 및 위젯 값을 지우고 첫 질문으로 이동."""
    for key in list(st.session_state.keys()):
        if key.startswith("radio_"):
            del st.session_state[key]
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.show_results = False


st.title("💜 나의 사랑의 언어")
st.caption("30개의 질문으로 알아보는 나의 애정 표현·수용 방식")

if not st.session_state.show_results:
    idx = st.session_state.current_question
    answered_count = len(st.session_state.answers)

    st.write(f"**응답 진행률: {answered_count} / {len(QUESTIONS)}문항**")
    st.progress(answered_count / len(QUESTIONS))
    st.caption(f"현재 {idx + 1} / {len(QUESTIONS)}번 질문")

    with st.container(border=True):
        st.subheader(f"Q{idx + 1}. 어떤 표현이 나에게 더 와닿나요?")
        st.write("둘 다 마음에 들더라도 **더 공감되는 한 가지**를 골라주세요.")

        options = [item[0] for item in QUESTIONS[idx]]
        codes = [item[1] for item in QUESTIONS[idx]]
        previous_code = st.session_state.answers.get(idx)
        previous_index = codes.index(previous_code) if previous_code in codes else None

        # 라디오 값은 표시 문장 대신 유형 코드로 관리해 채점을 단순화합니다.
        selected_code = st.radio(
            "답변 선택",
            options=codes,
            index=previous_index,
            format_func=lambda code: options[codes.index(code)],
            key=f"radio_{idx}",
            on_change=save_answer,
            args=(idx,),
            label_visibility="collapsed",
        )

    left, right = st.columns(2)
    with left:
        if st.button("← 이전 질문", disabled=(idx == 0), use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()
    with right:
        label = "테스트 완료 💜" if idx == len(QUESTIONS) - 1 else "다음 질문 →"
        if st.button(label, type="primary", use_container_width=True):
            # 응답하지 않은 질문은 통과할 수 없습니다.
            if selected_code is None:
                st.warning("다음으로 이동하려면 먼저 답변을 선택해 주세요.")
            else:
                st.session_state.answers[idx] = selected_code
                if idx == len(QUESTIONS) - 1:
                    if len(st.session_state.answers) == len(QUESTIONS):
                        st.session_state.show_results = True
                        st.rerun()
                    else:
                        st.warning("답변하지 않은 질문이 있어요. 이전 질문을 확인해 주세요.")
                else:
                    st.session_state.current_question += 1
                    st.rerun()

else:
    # PDF의 기준: 선택한 A/B/C/D/E의 횟수 = 해당 사랑의 언어 점수.
    scores = {code: 0 for code in LOVE_LANGUAGES}
    for code in st.session_state.answers.values():
        scores[code] += 1

    top_score = max(scores.values())
    top_codes = [code for code, score in scores.items() if score == top_score]
    main_names = ", ".join(LOVE_LANGUAGES[code]["name"] for code in top_codes)

    st.success("30개 질문을 모두 완료했어요! 🎉")
    with st.container(border=True):
        st.subheader("✨ 나의 대표 사랑의 언어")
        st.markdown(f"### {main_names}")
        if len(top_codes) > 1:
            st.caption("가장 높은 점수가 같아 공동 1위로 표시했어요.")
        st.write(f"가장 높은 점수는 **{top_score}점**입니다. (전체 30점)")

    st.subheader("📊 5가지 사랑의 언어 결과")
    chart_data = pd.DataFrame(
        [{"유형": info["name"], "점수": scores[code]}
         for code, info in LOVE_LANGUAGES.items()]
    ).set_index("유형")
    st.bar_chart(chart_data, color="#9b71dd", height=320)
    st.caption("각 문항의 선택은 해당 유형에 1점을 더합니다. 5개 점수의 합계는 30점입니다.")

    st.subheader("💟 유형별 설명")
    for code, info in LOVE_LANGUAGES.items():
        with st.container(border=True):
            st.markdown(f"**{info['emoji']} {info['name']} ({info['english']}) — {scores[code]}점**")
            st.write(info["description"])

    st.info("이 테스트는 스스로의 선호를 돌아보기 위한 참고 자료이며, 심리학적 진단 도구는 아닙니다.")
    if st.button("🔄 다시 검사하기", type="primary", use_container_width=True):
        restart()
        st.rerun()
