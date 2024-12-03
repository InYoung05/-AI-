import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = "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"  # OpenAI API 키를 입력하세요.

# Streamlit 페이지 구성
st.set_page_config(
    page_title="AI 기반 면접 준비 코칭",
    page_icon="🤖",
    layout="centered",
)

st.title("AI 기반 면접 준비 코칭 사이트")
st.header("면접 준비를 AI와 함께!")

# 사용자가 입력한 직업군
job = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

if job:
    with st.spinner("AI가 정보를 가져오고 있습니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 면접 준비 코치입니다."},
                    {"role": "user", "content": f"{job} 직업에 필요한 주요 자격증과 면접 준비 팁을 알려주세요."},
                ],
            )

            result = response.choices[0].message["content"]
            st.success("정보를 성공적으로 가져왔습니다!")
            st.subheader(f"{job} 직업 관련 정보")
            st.text_area("AI가 추천하는 자격증 및 면접 팁", value=result.strip(), height=300)

        except openai.error.AuthenticationError as e:
            st.error("API 키 인증 실패: 올바른 OpenAI API 키를 사용했는지 확인하세요.")
        except openai.error.RateLimitError as e:
            st.error("요청 한도를 초과했습니다. 나중에 다시 시도하세요.")
        except openai.error.OpenAIError as e:
            st.error("OpenAI와 통신 중 오류가 발생했습니다. 다시 시도하세요.")
            st.write(f"세부 정보: {e}")
        except Exception as e:
            st.error("알 수 없는 오류가 발생했습니다.")
            st.write(f"세부 정보: {e}")

# 부가적인 면접 준비 팁 섹션
st.sidebar.title("부가 정보")
st.sidebar.info("자신감 있는 태도, 명확한 의사소통, 관련 프로젝트 경험 공유 등도 중요합니다!")
st.sidebar.text("📌 팁: 모의 면접을 통해 실전 감각을 익히세요!")
