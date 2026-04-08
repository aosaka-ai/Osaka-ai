import streamlit as st
from google import genai
from google.genai import types

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osaka AI", page_icon="🤖")

# 2. تعريف الـ Client - لاحظ إضافة الـ API Version يدوياً للتأكد
if "client" not in st.session_state:
    try:
        st.session_state.client = genai.Client(
            api_key=st.secrets["GOOGLE_API_KEY"],
            http_options={'api_version': 'v1beta'} # نجبره يكلم النسخة التجريبية اللي فيها الفلاش
        )
    except Exception as e:
        st.error(f"خطأ في الـ Client: {e}")

# 3. واجهة المستخدم
st.title("🤖 Osaka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("إيه الأخبار في الـ NBE؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # التعديل هنا: نستخدم اسم الموديل بدون 'models/' لأن الـ Client بيضيفها تلقائياً
            # ونضع الـ system_instruction داخل الـ config مباشرة
            response = st.session_state.client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="أنت Osaka AI، مساعد تقني خبير. رد بلهجة مصرية."
                )
            )
            
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # لو الموديل لسه مش لاقيه، هنطبع الموديلات المتاحة عندك عشان نعرف السبب
            st.error(f"خطأ: {e}")
            if "404" in str(e):
                st.info("جاري فحص الموديلات المتاحة لمفتاحك...")
                models = st.session_state.client.models.list()
                available = [m.name for m in models]
                st.write(f"الموديلات المتاحة لك هي: {available}")
