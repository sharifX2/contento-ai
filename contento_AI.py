import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Contento AI", page_icon="🎬", layout="centered")

st.title("صانع المحتوى والسيناريو - Contento AI")
st.caption("صمم سيناريوهات فيديوهاتك واصنع أوامر مشاهد واقعية (AI Video Prompts)")

# جلب المفتاح تلقائياً من Secrets الخاصة بـ Streamlit Cloud
api_key = st.secrets.get("GEMINI_API_KEY")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("المنصة:", ["TikTok", "Instagram Reels", "YouTube Shorts"])
with col2:
    topic = st.text_input("موضوع الفيديو:", placeholder="مثال: أفضل 5 نصائح لتركيب PC")

tone = st.selectbox("نبرة الكلام:", ["حماسي", "تعليمي / احترافي", "فكاهي / ساخر", "قصصي / تشويقي"])

generate_btn = st.button("إنشاء السيناريو والمشاهد الواقعية", type="primary")

if generate_btn:
    if not api_key:
        st.error("مفتاح Gemini API غير معرف في إعدادات Streamlit Secrets!")
    elif not topic:
        st.warning("رجاءً اكتب موضوع الفيديو أولاً!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
Act as an expert AI Video Producer and Content Creator.
Topic: {topic}
Platform: {platform}
Tone: {tone}

Generate a complete video concept with two parts:

PART 1: ARABIC SCRIPT
- Hook (First 3 seconds)
- Spoken Voiceover Script (السيناريو المحكي)
- Top 5 Hashtags

PART 2: REALISTIC AI VIDEO PROMPTS (In English for Runway / Midjourney / Sora)
For each scene, provide detailed photorealistic AI generation prompts (Include camera angles, lighting, and movement).
"""
            with st.spinner("جاري توليد المحتوى والسيناريو..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
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