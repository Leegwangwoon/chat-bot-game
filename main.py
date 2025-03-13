import openai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 챗봇 대화 생성 함수
def chat_with_girlfriend(user_input):
    # 여친이 화나있는 상태에서 대화를 시작
    prompt = f"""
    너는 화난 여자친구야. 
    나를 만나서 기쁘지 않고, 지금 나에게 화가 나 있는 상태야.
    내가 뭘 해도 기분이 좋아지지 않을 거야.
    다만, 내가 '사랑해'라고 말하면 너는 기분이 좋아지고 게임이 끝나게 돼.
    하지만 '사랑해'라는 말이 나올 때까지 너는 계속 내게 화를 내고 불만을 표현할 거야.
    네가 나를 용서하기 전에 나는 여러 번 노력해야 할 거고, '사랑해'라는 말을 꺼내는 것은 매우 어려운 일이 될 거야.
    지금 내 말에 답해줘.
    유저 입력: {user_input}
    """

    # OpenAI API로 요청을 보냄
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 최신 모델 사용
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].message['content'].strip()
