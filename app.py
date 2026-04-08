import streamlit as st
from google import genai
from google.genai import types

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# 2. الربط بالمكتبة الجديدة
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # إنشاء Client
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"مشكلة في الـ API Key: {e}")
    st.stop()

# 3. شخصية Osaka AI
system_instruction = "أنت 'Osaka AI' مساعد تقني لبنك، خبير في 488 سيرفر و76 تطبيق بنكي. رد بلهجة مصرية تقنية."

st.title("🤖 Osaka AI")
st.subheader("IT Operations Smart Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("إيه المشكلة في السيرفرات؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # التعديل الجوهري: استخدام GenerateConfig الصحيح للمكتبة الجديدة
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
            )
            
            output_text = response.text
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            st.error(f"حصل خطأ فني: {str(e)}")
