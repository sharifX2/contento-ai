import sys
import os

# إجبار Python على استخدام ترميز UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
from google import genai

# إعدادات الصفحة
st.set_page_config(page_title="Contento AI", layout="centered")

# تنسيق بسيط بالـ CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Contento AI - صانع المحتوى والسيناريو الواقعي")
st.caption("صمم سيناريوهات فيديوهاتك واصنع أوامر مشاهد واقعية (AI Video Prompts)")

st.divider()

col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("المنصة:", ["TikTok", "Reels", "YouTube Shorts"])
    tone = st.selectbox("نبرة الكلام:", ["حماسي", "تعليمي", "كوميدي", "احترافي"])

with col2:
    api_key = st.text_input("مفتاح Gemini API:", type="password")
    topic = st.text_input("موضوع الفيديو:", placeholder="مثال: أفضل 5 نصائح لتركيب PC")

st.write("")
generate_btn = st.button("إنشاء السيناريو والمشاهد الواقعية")

if generate_btn:
    if not api_key:
        st.error("الرجاء إدخال مفتاح الـ API الأول!")
    elif not topic:
        st.warning("اكتب موضوع الفيديو الأول!")
    else:
        with st.spinner("جاري كتابة السيناريو وتصميم مشاهد AI واقعية..."):
            try:
                clean_api_key = api_key.strip()
                client = genai.Client(api_key=clean_api_key)
                
                prompt = f"""
                You are an expert AI content creator and cinematic director for {platform}.
                Topic: "{topic}".
                Tone: {tone}.
                
                Generate a complete video concept with two parts:
                
                PART 1: ARABIC SCRIPT
                - Hook (First 3 seconds)
                - Spoken Voiceover Script (السيناريو المحكي)
                - Top 5 Hashtags
                
                PART 2: REALISTIC AI VIDEO PROMPTS (In English for Runway / Midjourney / Sora)
                For each scene, provide detailed photorealistic AI generation prompts (Include camera angle, lighting, 8K resolution, photorealistic cinematic style, realistic lighting, octane render).
                """
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                )
                
                st.success("تم تجهيز السيناريو مع أوامر الفيديو الواقعي بنجاح!")
                st.markdown(response.text)
                st.divider()
                st.download_button(
                    label="تحميل الملف كامل",
                    data=response.text.encode('utf-8'),
                    file_name="script_and_prompts.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")