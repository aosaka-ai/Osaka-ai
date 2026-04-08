import streamlit as st
import google.generativeai as genai

# 1. إعداد مفتاح الربط (هتحتاج تجيب API Key مجاني من Google AI Studio)
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-pro')

st.title("🤖 Osaka AI - ITOps Assistant")
st.caption("مساعدك الذكي لإدارة الـ 488 سيرفر والخدمات البنكية")

# 2. تعريف "شخصية" الـ AI (الـ System Instruction)
system_prompt = """
أنت الآن Osaka AI، خبير IT Operations متخصص في البنوك. 
مهمتك مساعدة المهندسين في حل مشاكل السيرفرات (Windows/Linux)، 
والتعامل مع أعطال الـ ATM و POS، وتقديم حلول سريعة لأوامر OpenShift.
اجعل إجاباتك تقنية، مباشرة، وباللهجة المصرية التقنية.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المستخدم
if prompt := st.chat_input("إيه المشكلة اللي بتواجهك في السيرفرات؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الـ AI
    with st.chat_message("assistant"):
        full_prompt = f"{system_prompt}\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
§§
