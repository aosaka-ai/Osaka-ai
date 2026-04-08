import streamlit as st
from google import genai

# إعدادات الصفحة
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# الربط بالـ API (المكتبة الجديدة تستخدم Client)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"مشكلة في الـ API Key: {e}")
    st.stop()

# شخصية Osaka AI
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
            # طريقة النداء الجديدة في المكتبة الحديثة
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                config={'system_instruction': system_instruction},
                contents=prompt
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ في الربط: {str(e)}")
