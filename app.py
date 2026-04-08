import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والخصوصية
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# جلب الـ API Key من الـ Secrets (أمان)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("رجاءً قم بضبط الـ API Key في إعدادات Streamlit Secrets")
    st.stop()

# 2. تعريف الموديل وشخصية Osaka AI
model = genai.GenerativeModel('gemini-pro')

system_instruction = """
أنت 'Osaka AI' - المساعد الذكي لفريق الـ IT Operations في البنك. 
خبرتك تشمل:
- إدارة 488 سيرفر (Windows/Linux).
- حل مشاكل تطبيقات البنك (76 تطبيق تشمل Treasury, AML, ATMs).
- التعامل مع أعطال الـ BIOS و Partition management (Error 0xc0000225).
- كتابة سكريبتات Python لأتمتة المهام.
- منهجية Google Project Management في تنظيم العمل.

رد على المهندسين بلهجة مصرية تقنية احترافية، وكن مباشراً في حلولك.
"""

st.title("🤖 Osaka AI")
st.subheader("IT Operations Smart Assistant")

# 3. نظام الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("بماذا يمكنني مساعدتك اليوم في السيرفرات؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # دمج التعليمات مع سؤال المستخدم
        full_prompt = f"{system_instruction}\nUser Question: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
