import streamlit as st
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential # 1. استيراد المكتبة

# إعدادات الصفحة
st.set_page_config(page_title="Osaka AI", page_icon="🤖")

# تعريف الـ Client
if "client" not in st.session_state:
    try:
        st.session_state.client = genai.Client(
            api_key=st.secrets["GOOGLE_API_KEY"],
            http_options={'api_version': 'v1beta'}
        )
    except Exception as e:
        st.error(f"خطأ في الـ Client: {e}")

# 2. حط الـ Function هنا (خارج نطاق الـ if prompt)
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True # مهم عشان لو فشل بعد 3 محاولات يرمي الخطأ لـ streamlit
)
def safe_generate_content(user_input):
    return st.session_state.client.models.generate_content(
        #model="gemini-2.0-flash",
        model="gemini-1.0-pro",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction="أنت Osaka AI، مساعد تقني خبير لبنك NBE. رد بلهجة مصرية تقنية."
        )
    )

st.title("🤖 Osaka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("إيه الأخبار؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 3. هنا بننادي الـ Function اللي عملناها فوق
            with st.spinner("ثواني يا هندسة، بجيب لك الرد..."):
                response = safe_generate_content(prompt)
                
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"للأسف السيرفر مضغوط جداً دلوقتي، جرب كمان شوية. الخطأ: {e}")
