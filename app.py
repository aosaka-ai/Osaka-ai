import streamlit as st
from google import genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# 2. الربط بالمكتبة الجديدة (Client)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # إنشاء Client بيستخدم v1 المستقرة تلقائياً
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"مشكلة في الـ API Key: {e}")
    st.stop()

# 3. شخصية Osaka AI
system_instruction = """
أنت 'Osaka AI' - المساعد الذكي لفريق الـ IT Operations في البنك. 
خبرتك في إدارة 488 سيرفر و76 تطبيق بنكي. 
رد بلهجة مصرية تقنية احترافية.
"""

st.title("🤖 Osaka AI")
st.subheader("IT Operations Smart Assistant")

# 4. نظام الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("إيه المشكلة اللي مقابلاك في السيرفرات؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # الطريقة الصحيحة للمكتبة الجديدة google-genai
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                config={
                    'system_instruction': system_instruction,
                    'temperature': 0.7
                },
                contents=prompt
            )
            
            output_text = response.text
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            # طباعة الخطأ بشكل أوضح للـ Troubleshooting
            st.error(f"حصل خطأ فني: {str(e)}")
