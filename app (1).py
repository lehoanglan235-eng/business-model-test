"""Love Language: 30문항 사랑의 언어 테스트 (Streamlit 단일 파일)

실행 방법
    pip install streamlit matplotlib
    streamlit run app.py

문항: 사용자가 제공한 Love Languages Test PDF를 한국어로 번역.
결과 설명: 사용자가 제공한 Five Love Languages 인포그래픽의 항목을 번역·요약.
"""

import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="나의 사랑의 언어 | Love Language", page_icon="💜", layout="wide", initial_sidebar_state="expanded")

# PDF 기준 유형 코드. 각 문항마다 둘 중 하나를 고르면 해당 유형에 1점이 더해집니다.
LANGUAGES = {
    "A": {
        "name": "인정하는 말", "english": "Words of Affirmation", "emoji": "💬", "color": "#B28AE6",
        "short": "칭찬, 격려, 감사처럼 진심이 담긴 말에서 사랑을 느껴요.",
        "detail": "당신에게는 상대방의 따뜻한 말 한마디가 큰 힘이 됩니다. 노력과 장점을 알아봐 주고, 진심으로 감사와 애정을 표현할 때 자신이 소중한 사람이라는 확신을 얻습니다. 말의 내용뿐 아니라 진정성과 공감도 중요하게 여깁니다.",
        "communication": "격려하고, 인정하고, 감사를 표현해 주세요. 감정에 공감하면서 이야기를 적극적으로 들어주는 대화가 좋습니다.",
        "actions": "예상치 못한 응원 메시지나 손편지를 보내고, 고맙거나 멋진 점을 구체적으로 자주 말해 주세요.",
        "avoid": "도움이 되지 않는 비난, 애쓴 노력을 알아주지 않는 태도, 감사 표현을 생략하는 행동은 상처가 될 수 있어요.",
    },
    "B": {
        "name": "함께하는 시간", "english": "Quality Time", "emoji": "⏰", "color": "#8E6BD1",
        "short": "방해받지 않고 서로에게 집중하는 시간을 중요하게 생각해요.",
        "detail": "당신은 단순히 같은 공간에 있는 것보다 서로에게 집중하는 시간을 통해 친밀함을 느낍니다. 눈을 맞추고 이야기를 나누거나 작은 활동을 함께하는 순간이 특별합니다. 얼마나 오래 만나는지뿐 아니라, 그 시간에 얼마나 마음을 쏟는지가 중요합니다.",
        "communication": "다른 일을 잠시 멈추고 온전히 집중해 대화해 주세요. 방해받지 않는 일대일 시간이 특히 중요합니다.",
        "actions": "함께 산책하거나 소소한 활동을 해 보세요. 둘만의 특별한 순간과 주말 나들이를 계획하는 것도 좋습니다.",
        "avoid": "함께 있을 때 스마트폰 등에 계속 주의를 빼앗기거나, 오랫동안 단둘이 시간을 보내지 않는 것을 피해 주세요.",
    },
    "C": {
        "name": "선물 받기", "english": "Receiving Gifts", "emoji": "🎁", "color": "#79AEE8",
        "short": "선물에 담긴 기억, 마음과 정성을 사랑의 표시로 받아들여요.",
        "detail": "당신에게 선물은 가격표가 아니라 '나를 생각해 주었구나'라는 마음의 증거입니다. 작지만 취향을 고려한 물건, 우연히 떠올라 준비한 기념품, 직접 만든 선물처럼 사연과 의미가 있는 표현에서 깊은 감동을 느낍니다.",
        "communication": "상대의 취향을 기억하고 세심하게 배려하며, 의미 있는 말과 행동으로 마음을 표현해 주세요.",
        "actions": "크지 않아도 정성 어린 선물이나 작은 깜짝 이벤트를 준비해 보세요. 선물을 받았을 때 감사도 표현해 주세요.",
        "avoid": "생일이나 기념일 같은 특별한 날을 잊거나, 선물을 성의 없이 주고받는 태도는 서운함을 줄 수 있어요.",
    },
    "D": {
        "name": "실제 행동", "english": "Acts of Service", "emoji": "🛠️", "color": "#647994",
        "short": "말보다 실질적인 도움과 배려하는 행동에서 사랑을 느껴요.",
        "detail": "당신은 상대가 시간을 내어 실제로 도와줄 때 깊은 애정을 느낍니다. 힘든 집안일을 함께 하거나 바쁜 일정을 배려해 주는 등 일상 속의 작은 실천이 사랑의 언어가 됩니다. 특히 약속을 지키고 꾸준히 행동으로 보여 주는 것이 중요합니다.",
        "communication": "'내가 도와줄게'처럼 구체적인 행동을 제안하고, 함께 문제를 해결하는 동반자라는 느낌을 전해 주세요.",
        "actions": "집안일을 나눠 하거나 아침 식사를 준비하고, 일상의 부담을 덜어 줄 일을 먼저 찾아 실천해 보세요.",
        "avoid": "상대의 부탁을 늘 뒷전으로 미루거나, 크고 작은 약속을 지키지 않는 태도는 피하는 것이 좋습니다.",
    },
    "E": {
        "name": "스킨십", "english": "Physical Touch", "emoji": "🫶", "color": "#6DBDAA",
        "short": "서로 편안하게 동의한 신체 접촉에서 애정과 안정감을 느껴요.",
        "detail": "당신은 다정한 포옹이나 손잡기처럼 친밀한 신체 접촉을 통해 사랑과 유대감을 느낍니다. 말하지 않아도 전해지는 따뜻함과 곁에 있다는 감각이 큰 위로가 됩니다. 모든 접촉은 서로의 의사와 경계를 존중하며 이루어질 때 더 의미 있습니다.",
        "communication": "상대가 편안해하는지 살피며 몸짓과 다정한 접촉으로 애정을 표현해 주세요.",
        "actions": "서로 동의할 때 포옹, 손잡기, 가벼운 어깨 토닥임 등 일상적인 신체적 애정을 나눠 보세요.",
        "avoid": "상대가 원하는 애정 표현을 무시하거나, 오랫동안 신체적 친밀감에 소홀하거나, 애정 표현을 차갑게 대하는 태도를 피하세요.",
    },
}

# PDF 1~3쪽의 원문 30개 문항을 순서대로 옮긴 한국어 번역입니다.
# (보이는 문장, 사랑의 언어 코드) 쌍 2개로 각 문항을 저장합니다.
# 주의: 원문 PDF의 7번 두 번째 문항은 기호가 E지만, 문장 의미상 '인정하는 말(A)'입니다.
# 따라서 7번 두 번째 선택지는 A로 채점합니다. (원문 오기로 판단한 명시적 보정)
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

# 모든 유형이 선택지에 12회씩 등장하는지 확인할 수 있습니다.
assert len(QUESTIONS) == 30 and all(len(q) == 2 for q in QUESTIONS)
assert all(sum(code == category for q in QUESTIONS for _, code in q) == 12 for category in LANGUAGES)

# 전역 스타일: 밝은 보라색 + 문항 카드. 사이드바의 숫자 버튼은 원형으로 표시합니다.
st.markdown("""
<style>
.stApp { background: linear-gradient(155deg, #fcf9ff 0%, #f5edff 60%, #ffffff 100%); }
.block-container { max-width: 1030px; padding-top: 2rem; padding-bottom: 3rem; }
h1, h2, h3 { color: #654293 !important; }
[data-testid="stSidebar"] { background: #f6efff; }
[data-testid="stSidebar"] .stButton > button { min-height: 2.3rem; }
/* 숫자 네비게이션: 둥근 원, 미응답은 흰색 */
[class^="st-key-nav_"] button, [class*=" st-key-nav_"] button {
    width: 2.25rem !important; height: 2.25rem !important;
    min-height: 2.25rem !important; padding: 0 !important;
    border-radius: 50% !important; border: 1.5px solid #d2b9f3 !important;
    background: white !important; color: #7351a7 !important;
    font-weight: 700 !important; margin: 0 auto !important;
}
[class^="st-key-nav_"] button, [class*=" st-key-nav_"] button:hover { border-color: #7d51c5 !important; transform: translateY(-1px); }
/* 응답 완료(보라 원) / 현재 질문(두꺼운 테두리)은 아래에서 별도 CSS로 덮어씌웁니다. */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important; border: 1px solid #e8daf9 !important;
    background: rgba(255,255,255,.96);
    box-shadow: 0 8px 25px rgba(107,70,158,.07);
}
div.stButton > button[kind="primary"] { background: #8d5bd0; color: white; border-color: #8d5bd0; border-radius: 12px; }
div.stButton > button:not([kind="primary"]) { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# 페이지 모드: intro / quiz / result. session_state는 질문 페이지를 바꾸어도 유지됩니다.
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}  # {문항 인덱스: 유형 코드}


def start_test():
    st.session_state.page = "quiz"
    st.session_state.current_question = 0


def go_to_question(index: int):
    # 무응답이어도 원하는 문항으로 이동할 수 있습니다.
    st.session_state.current_question = index


def previous_question():
    st.session_state.current_question = max(0, st.session_state.current_question - 1)


def next_question():
    st.session_state.current_question = min(29, st.session_state.current_question + 1)


def save_answer(index: int):
    """문항별 라디오 변경 시 응답 내용을 저장합니다."""
    code = st.session_state.get(f"answer_{index}")
    if code is not None:
        st.session_state.answers[index] = code


def finish_test():
    """미응답이 하나라도 있으면 결과 화면으로 이동하지 않습니다."""
    if len(st.session_state.answers) == len(QUESTIONS):
        st.session_state.page = "result"


def restart_test():
    """라디오 위젯의 값까지 전부 지워 첫 소개 화면부터 다시 시작합니다."""
    for key in list(st.session_state):
        if key.startswith("answer_"):
            del st.session_state[key]
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.page = "intro"


def render_intro():
    st.title("💜 당신의 Love Language가 무엇입니까?")
    st.markdown("### 사랑을 느끼는 방식은 사람마다 다릅니다")
    with st.container(border=True):
        st.write(
            "**사랑의 언어(Love Languages)** 는 작가이자 관계 상담가인 **게리 채프먼(Gary Chapman)** 이 "
            "책 《The 5 Love Languages》에서 널리 알린 개념입니다. "
            "사람마다 사랑을 주고받을 때 특히 중요하게 여기는 표현 방식이 다르다는 생각에서 출발합니다."
        )
        st.write(
            "이 테스트에서는 총 **30개의 질문**마다 두 문장 중 자신에게 더 잘 맞는 문장을 선택합니다. "
            "답변을 모아 가장 선호하는 사랑의 표현 방식을 알아볼 수 있어요. 정답이나 오답은 없습니다."
        )
    st.subheader("🌷 사랑의 언어 5가지")
    for code, info in LANGUAGES.items():
        with st.container(border=True):
            st.markdown(f"**{info['emoji']} {info['name']} ({info['english']})**")
            st.write(info["short"])
    st.caption("※ 자기 이해와 대화를 돕는 참고용 테스트이며, 임상적 심리 진단은 아닙니다.")
    st.button("바로 테스트 하기 ➡️", type="primary", use_container_width=True, on_click=start_test)


def render_navigation():
    """사이드바에 정확히 6행 × 5열의 클릭 가능한 문항 번호를 표시합니다."""
    count = len(st.session_state.answers)
    with st.sidebar:
        st.markdown("### 💜 문항 바로가기")
        st.caption("번호를 누르면 해당 질문으로 이동합니다.")
        st.progress(count / 30)
        st.markdown(f"**{count} / 30문항 응답 완료**")

        # 버튼마다 고유한 key가 있으므로 CSS로 응답 여부를 구분할 수 있습니다.
        styles = []
        for row in range(6):
            columns = st.columns(5, gap="small")
            for col in range(5):
                number = row * 5 + col + 1
                index = number - 1
                with columns[col]:
                    st.button(str(number), key=f"nav_{number}", use_container_width=True,
                              on_click=go_to_question, args=(index,))
                if index in st.session_state.answers:
                    styles.append(f'.st-key-nav_{number} button {{background: #9666d4 !important; color: white !important; border-color: #9666d4 !important;}}')
                if index == st.session_state.current_question and st.session_state.page == "quiz":
                    styles.append(f'.st-key-nav_{number} button {{outline: 2px solid #5f369f !important; outline-offset: 2px !important;}}')
        st.markdown("<style>" + "\n".join(styles) + "</style>", unsafe_allow_html=True)
        st.caption("🟣 응답 완료  |  ⚪ 미응답")
        if st.button("처음부터 다시 검사하기", use_container_width=True, key="restart_sidebar"):
            restart_test()
            st.rerun()


def render_quiz():
    render_navigation()
    index = st.session_state.current_question
    count = len(st.session_state.answers)
    st.title("💜 나의 사랑의 언어 테스트")
    st.write(f"**응답 진행률: {count} / 30**")
    st.progress(count / 30)
    st.caption(f"질문 {index + 1} / 30 · 다른 질문으로 이동해도 응답이 저장됩니다.")

    with st.container(border=True):
        st.subheader(f"Q{index + 1}. 나에게 더 잘 맞는 문장은?")
        st.write("두 문장이 모두 마음에 들어도 **더 공감되는 하나**를 선택해 주세요.")
        options = QUESTIONS[index]
        codes = [code for _, code in options]
        radio_key = f"answer_{index}"
        # 페이지에 다시 왔을 때 기존 응답이 그대로 선택되도록 복원합니다.
        if radio_key not in st.session_state:
            st.session_state[radio_key] = st.session_state.answers.get(index)
        st.radio(
            "한 문장 선택", options=codes, index=None, key=radio_key,
            format_func=lambda code: next(text for text, item_code in options if item_code == code),
            on_change=save_answer, args=(index,), label_visibility="collapsed",
        )

    left, right = st.columns(2)
    with left:
        st.button("⬅️ 이전 질문", disabled=(index == 0), use_container_width=True,
                  on_click=previous_question)
    with right:
        if index < 29:
            st.button("다음 질문 ➡️", type="primary", use_container_width=True,
                      on_click=next_question)
        else:
            if st.button("테스트 완료 💜", type="primary", use_container_width=True):
                if count < 30:
                    missing = [str(i + 1) for i in range(30) if i not in st.session_state.answers]
                    st.warning("모든 문항에 답해야 결과를 볼 수 있어요. 미응답 문항: " + ", ".join(missing))
                else:
                    finish_test()
                    st.rerun()
    if count == 30 and index != 29:
        st.success("모든 문항에 답했어요! 30번 문항으로 이동해 '테스트 완료'를 눌러주세요.")


def render_results():
    # 채점: A~E 응답 수를 센 뒤 가장 높은 코드(동점인 경우 복수)를 찾습니다.
    scores = {code: sum(answer == code for answer in st.session_state.answers.values())
              for code in LANGUAGES}
    high_score = max(scores.values())
    winners = [code for code, score in scores.items() if score == high_score]

    st.title("💜 나의 사랑의 언어 결과")
    st.success("30개 질문에 모두 응답했습니다!")
    with st.container(border=True):
        st.subheader("📊 사랑의 언어 비율")
        fig, ax = plt.subplots(figsize=(7, 4.7))
        fig.patch.set_facecolor("white")
        vals = [scores[code] for code in LANGUAGES]
        colors = [info["color"] for info in LANGUAGES.values()]
        ax.pie(vals, colors=colors, startangle=90, counterclock=False,
               autopct=lambda p: f"{p:.1f}%" if p >= 3.0 else "",
               pctdistance=0.75, textprops={"color": "white", "fontsize": 11, "weight": "bold"},
               wedgeprops={"edgecolor": "white", "linewidth": 2})
        ax.axis("equal")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        # 한글 글꼴 이슈를 피하려고 범례는 Streamlit 텍스트로 표시합니다.
        legend = "".join(
            f'<span style="display:inline-block;margin:0 15px 9px 0;white-space:nowrap">'
            f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{info["color"]};margin-right:6px"></span>'
            f'{info["name"]} <b>{scores[code]}점</b></span>'
            for code, info in LANGUAGES.items()
        )
        st.markdown(legend, unsafe_allow_html=True)
        st.caption("점수 합계 30점 · 원그래프의 비율은 전체 30개 응답 중 해당 유형을 선택한 비율입니다.")

    # 사용자 요청: 그래프 바로 아래 결과 문구 및 결과 유형만 구체적으로 설명.
    if len(winners) == 1:
        winner_name = LANGUAGES[winners[0]]["name"]
        st.markdown(f"## ✨ 당신은 **{winner_name}** 유형입니다!")
    else:
        combined = " · ".join(LANGUAGES[code]["name"] for code in winners)
        st.markdown(f"## ✨ 당신은 **{combined}** 유형입니다!")
        st.info("최고 점수가 같아 여러 유형이 공동 1위로 나타났습니다.")

    for code in winners:
        info = LANGUAGES[code]
        with st.container(border=True):
            st.subheader(f"{info['emoji']} {info['name']} ({info['english']})")
            st.write(info["detail"])
            st.markdown("**💬 어떻게 소통하면 좋을까요?**")
            st.write(info["communication"])
            st.markdown("**💞 사랑을 표현하는 행동**")
            st.write(info["actions"])
            st.markdown("**⚠️ 피하면 좋은 행동**")
            st.write(info["avoid"])
    st.caption("이 결과는 자신을 이해하기 위한 참고 자료이며, 개인의 성향을 확정하는 진단이 아닙니다.")
    if st.button("🔄 다시 테스트하기", type="primary", use_container_width=True):
        restart_test()
        st.rerun()


# 첫 페이지에는 테스트 버튼을 누르기 전까지 질문이나 문항 네비게이션을 표시하지 않습니다.
if st.session_state.page == "intro":
    render_intro()
elif st.session_state.page == "quiz":
    render_quiz()
else:
    render_results()
