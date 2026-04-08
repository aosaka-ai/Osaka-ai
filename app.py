import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osaka AI - ITOps", page_icon="🤖")

# 2. الربط بالـ API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("فيه مشكلة في الـ API Key جوه الـ Secrets!")
    st.stop()

# 3. تعريف الموديل (استخدام الاسم المباشر هو الأضمن)
# جربنا Flash و Pro، خلينا نثبت على Flash بأحدث تعريف له
model = genai.GenerativeModel('gemini-1.5-flash')

system_instruction = """
أنت 'Osaka AI' - المساعد الذكي لفريق الـ IT Operations في البنك. 
خبرتك تشمل إدارة 488 سيرفر، حل مشاكل 76 تطبيق بنكي، وحل أخطاء الـ BIOS والـ Partitions.
رد باللهجة المصرية التقنية وبسرعة.
"""

st.title("🤖 Osaka AI")
st.subheader("IT Operations Smart Assistant")

# 4. نظام الدردشة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المستخدم
if prompt := st.chat_input("إيه المشكلة اللي مقابلاك في السيرفرات؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هنا بنبعت الـ System Instruction مع كل سؤال عشان يحافظ على شخصيته
            full_prompt = f"{system_instruction}\n\nالمستخدم يسأل: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حصل خطأ فني في الربط: {str(e)}")
