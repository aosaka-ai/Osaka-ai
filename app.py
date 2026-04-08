import streamlit as st
from google import genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# 2. الربط بالمكتبة الجديدة
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # إجبار الـ Client على استخدام الإصدار المستقر v1
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
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
            # استخدام اسم الموديل الكامل لضمان التوافق
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                config={'system_instruction': system_instruction},
                contents=prompt
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("الموديل مرجعش رد، جرب تاني.")
                
        except Exception as e:
            # لو لسه فيه 404، هنحاول نستخدم الموديل البديل فوراً (Failover)
            try:
                response = client.models.generate_content(
                    model="gemini-1.0-pro",
                    config={'system_instruction': system_instruction},
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e2:
                st.error(f"خطأ فني مستمر: {str(e2)}")
