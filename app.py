import streamlit as st
from main import chat_with_girlfriend  # 백엔드에서 함수 불러오기
from streamlit_chat import message  # 대화 출력용 라이브러리
import base64
import os

# 스트림릿 UI 설정
st.set_page_config(page_title="이 별에 이별에서 이별하라!", layout="wide")

# 함수: 이미지 파일을 Base64로 인코딩
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 함수: 배경 이미지 설정
def set_background(image_path):
    bin_str = get_base64_of_bin_file(image_path)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: 40% auto; 
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# 함수: 오디오 파일 재생 (Base64로 인코딩)
def play_audio(audio_file):
    if os.path.exists(audio_file):
        audio_bytes = get_base64_of_bin_file(audio_file)
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/wav;base64,{audio_bytes}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        <script>
            var audio = document.querySelector('audio');
            audio.volume = 0.5;  // 볼륨을 50%로 설정
            audio.play().catch(function(error) {{
                console.log("Audio playback failed: ", error);
            }});
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error("오디오 파일을 찾을 수 없습니다. 경로를 확인해주세요!")

# 로컬 이미지 경로 설정
image_path = "kakao.jpg"  # 이미지가 동일한 디렉토리에 있는지 확인
audio_path = "ka.wav"  # 오디오 파일 경로

# 배경 이미지 설정
if os.path.exists(image_path):
    set_background(image_path)
else:
    st.error("이미지를 찾을 수 없습니다. 경로를 확인해주세요!")

st.title("이 별에 이별에서 이별하라!")

# 사용자 이름 입력 (옵션)
user_name = st.text_input("이름을 입력하세요:", "")

# 게임 승리 체크 변수
if 'won' not in st.session_state:
    st.session_state.won = False

# 대화 기록 초기화 (세션 상태 사용)
if 'history' not in st.session_state:
    st.session_state.history = []

# 대화 입력 필드
user_input = st.text_input("대화를 입력하세요:", "")

# 유저 입력이 있을 경우
if user_input:
    # 대화 기록에 유저 입력 추가
    st.session_state.history.append({"role": "user", "content": user_input})

    # 챗봇 응답 생성 (백엔드 함수 호출)
    chatbot_response = chat_with_girlfriend(user_input)

    # 응답에 '사랑해'가 포함되어 있으면 게임 종료
    if "사랑해" in chatbot_response:
        st.session_state.won = True

    # 챗봇의 대화 기록 추가
    st.session_state.history.append({"role": "assistant", "content": chatbot_response})

    # AI 응답 시 오디오 재생
    play_audio(audio_path)

# 게임 승리 여부 체크
if st.session_state.won:
    st.success("🎉 축하합니다! 여자친구가 '사랑해'라고 말해서 게임에 이겼어요! 🎉")
else:
    # 대화 출력
    with st.container():
        st.markdown("""
            <style>
                .chat-container {
                    background-color: rgba(255, 255, 255, 0.7);
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    max-width: 80%;  /* 채팅 컨테이너의 최대 너비를 80%로 설정 */
                    margin-left: auto;
                    margin-right: auto;
                }
                .stChatMessage {
                    background-color: rgba(0, 0, 0, 0.1) !important;
                    border-radius: 15px !important;
                    padding: 10px !important;
                    margin-bottom: 10px !important;
                }
                .stChatMessage .content p {
                    color: black !important;
                }
            </style>
            <div class="chat-container">
        """, unsafe_allow_html=True)

        for i, msg in enumerate(st.session_state.history):
            if msg["role"] == "user":
                message(msg['content'], is_user=True, key=f"user_{i}")
            else:
                message(msg['content'], is_user=False, key=f"assistant_{i}")

        st.markdown('</div>', unsafe_allow_html=True)

# 게임 재시작 버튼
if st.session_state.won and st.button("다시 시작"):
    st.session_state.won = False
    st.session_state.history = []
    st.experimental_rerun()

# 오디오 재생 테스트 버튼
if st.button("오디오 재생 테스트"):
    play_audio(audio_path)

