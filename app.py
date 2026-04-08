import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# الربط بالـ API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key missing!")
    st.stop()

# التعديل الجوهري هنا: نداء الموديل بدون كلمة models/ وبدون تحديد إصدار
model = genai.GenerativeModel('gemini-1.5-flash')

# نظام الدردشة البسيط
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
            # نداء مباشر وبسيط
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # هنا هنطبع الخطأ كامل عشان لو فشل نعرف السبب "الحقيقي"
            st.error(f"Error: {str(e)}")
