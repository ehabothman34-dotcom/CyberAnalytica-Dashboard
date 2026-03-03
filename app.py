import streamlit as st
import hashlib
import pandas as pd
import numpy as np
from datetime import datetime

# إعدادات واجهة CyberAnalytica الاحترافية
st.set_page_config(page_title="CyberAnalytica Pro Dashboard", layout="wide")

st.title("🛡️ منصة CyberAnalytica للتدقيق الذكي والرقابة الرقمية")
st.sidebar.image("https://via.placeholder.com/150", caption="CyberAnalytica 2026") # يمكنك وضع لوجو مدونتك هنا
st.sidebar.markdown("---")

menu = st.sidebar.selectbox("اختر وحدة التدقيق:", 
    ["📊 تدقيق ملفات القيود (Excel/CSV)", 
     "🧠 كشف الاحتيال بالذكاء الاصطناعي", 
     "🛡️ مراقبة تسريب البيانات التراكمي"])

# --- الوحدة الأولى: تدقيق الملفات المرفوعة ---
if menu == "📊 تدقيق ملفات القيود (Excel/CSV)":
    st.header("🔗 نظام ضمان نزاهة البيانات الضخم")
    uploaded_file = st.file_uploader("ارفع ملف القيود المحاسبية (CSV أو Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("معاينة البيانات:", df.head())
        
        if st.button("توليد بصمة رقمية لكل قيد"):
            # توليد Hash لكل سطر لضمان عدم التلاعب مستقبلاً
            df['Digital_Signature'] = df.apply(lambda row: hashlib.sha256(str(row).encode()).hexdigest(), axis=1)
            st.success("تم تشفير القيود بنجاح!")
            st.dataframe(df)
            st.info("💡 هذه البصمة تُستخدم لمطابقة البيانات في التدقيق القادم؛ أي تغيير في البيانات سيؤدي لاختلاف البصمة.")

# --- الوحدة الثانية: كشف الاحتيال الذكي (Anomaly Detection) ---
elif menu == "🧠 كشف الاحتيال بالذكاء الاصطناعي":
    st.header("👤 محرك كشف السلوكيات المشبوهة")
    st.write("تحليل الفواصل الزمنية لمحاولات الدخول باستخدام الانحراف المعياري المتقدم.")
    
    raw_data = st.text_input("أدخل أوقات العمليات بالثواني (مثال: 12, 15, 14, 2, 15):", "12, 15, 14, 2, 15")
    
    if st.button("تحليل النمط"):
        data = np.array([float(x) for x in raw_data.split(",")])
        mean = np.mean(data)
        std = np.std(data)
        
        # تحديد القيم الشاذة (التي تبعد أكثر من انحرافين معياريين)
        outliers = data[(data < mean - 2*std) | (data > mean + 2*std)]
        
        col1, col2 = st.columns(2)
        col1.metric("متوسط وقت العمليات", f"{mean:.2f} ثانية")
        col2.metric("مستوى التذبذب (Std)", f"{std:.2f}")
        
        if len(outliers) > 0:
            st.error(f"🚨 تنبيه: تم اكتشاف {len(outliers)} عمليات مشبوهة (خارج النمط الطبيعي)!")
            st.write("القيم المشبوهة:", outliers)
        else:
            st.success("✅ جميع العمليات تقع ضمن النمط البشري الطبيعي.")

# --- الوحدة الثالثة: المراقبة التراكمية ---
elif menu == "🛡️ مراقبة تسريب البيانات التراكمي":
    st.header("☁️ نظام منع تسريب البيانات (DLP)")
    
    if 'total_egress' not in st.session_state:
        st.session_state.total_egress = 0
    
    server = st.selectbox("الخادم المستهدف:", ["قاعدة بيانات الرواتب", "سيرفر التقارير"])
    transfer_size = st.number_input("حجم النقل الحالي (MB):", min_value=0)
    
    if st.button("تسجيل عملية النقل"):
        st.session_state.total_egress += transfer_size
        st.write(f"إجمالي البيانات الخارجة اليوم: {st.session_state.total_egress} MB")
        
        if st.session_state.total_egress > 1000: # حد 1 جيجا بايت تراكمي
            st.error("🚨 خطر! تم تجاوز الحد اليومي المسموح به لنقل البيانات الإجمالية.")
        elif transfer_size > 500:
            st.warning("⚠️ تنبيه: هذه العملية منفردة بحجم كبير، تم تسجيلها للتدقيق.")
        else:
            st.success("✅ عملية نقل آمنة.")

st.markdown("---")
st.caption(f" مدونة CyberAnalytica | {datetime.now().year}")

