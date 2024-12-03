import openai
import streamlit as st

# OpenAI API Key 설정
openai.api_key = 'your-openai-api-key'

# 면접 팁 요청 함수
def get_interview_tips(job_title):
    prompt = f"면접 준비를 위한 유용한 팁을 제공해주세요. 직업: {job_title}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# 직업 관련 자격증 정보 요청 함수
def get_certifications(job_title):
    prompt = f"{job_title}에 필요한 자격증과 관련 정보를 알려주세요."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# Streamlit 페이지 구성
def main():
    st.title("AI 기반 면접 준비 코칭 사이트")
    
    # 직업 선택
    job_title = st.text_input("면접을 준비할 직업을 입력하세요 (예: 소프트웨어 개발자, 마케팅 매니저 등):")
    
    if job_title:
        st.subheader(f"{job_title} 면접 준비 팁")
        interview_tips = get_interview_tips(job_title)
        st.write(interview_tips)
        
        st.subheader(f"{job_title} 관련 자격증 정보")
        certifications = get_certifications(job_title)
        st.write(certifications)
