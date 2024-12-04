import streamlit as st
import openai

# 앱 제목
st.title("AI Interview Tip")
st.subheader("직업별 맞춤 면접 준비 정보를 확인해보세요!")

# OpenAI API 키 입력
api_key = st.text_input("OpenAI API 키를 입력하세요", type="password", placeholder="API 키를 입력 후 Enter를 누르세요")

# OpenAI API 키 설정
if api_key:
    openai.api_key = api_key
else:
    st.warning("API 키를 입력해야 앱을 사용할 수 있습니다.")

# 직업 입력
job_input = st.text_input("면접 준비를 원하는 직업을 입력하세요", placeholder="예: 데이터 분석가, 소프트웨어 엔지니어 등")

# 질문 생성 함수
def generate_interview_tips(api_key, job):
    openai.api_key = api_key  # 입력된 API 키로 설정
    prompt = f"""
    Provide specific and practical interview preparation tips for the job role '{job}'. 
    Include tips on technical skills, soft skills, typical interview questions, and preparation strategies.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=700,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# 버튼 클릭 시 정보 생성
if st.button("면접 준비 정보 가져오기"):
    if not api_key:
        st.error("API 키를 먼저 입력해주세요!")
    elif not job_input.strip():
        st.warning("직업을 입력해주세요!")
    else:
        with st.spinner(f"'{job_input}'에 대한 정보를 생성 중입니다..."):
            try:
                tips = generate_interview_tips(api_key, job_input)
                st.success(f"'{job_input}' 직업에 대한 면접 준비 정보:")
                st.markdown(tips)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

# 하단 추가 정보
st.info("💡 원하는 직업 키워드를 입력하세요. 예: 'AI 엔지니어', '마케팅 전문가', '회계사'")
