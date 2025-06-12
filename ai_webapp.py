import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
import os
from dotenv import load_dotenv

# โหลด environment variables เพื่อเอา api-key จากไฟล์ .env 
load_dotenv()

st.title("Analytica-X AI")

# ======= อัปโหลด CSV =======
uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV ที่นี่", type=["csv"])
data = None

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("เนื้อหาจากไฟล์ CSV:")
    st.dataframe(data)

# ======= ป้อนคำสั่งผ่าน Text Input =======
user_query = st.text_input("พิมพ์คำสั่ง/คำถามที่คุณอยากถามเกี่ยวกับข้อมูล:")

# ======= รัน LLM ถ้าทั้งไฟล์ CSV และคำถามพร้อม =======
if uploaded_file is not None and user_query:
    # ดึง API key
    groq_api_key = os.getenv('GROQ_API_KEY')

    # สร้างโมเดล LLM จาก Groq
    llm = ChatGroq(model_name='llama3-8b-8192', api_key=groq_api_key)

    # ใช้ SmartDataframe เชื่อมกับ LLM
    smart_df = SmartDataframe(data, config={'llm': llm, "save_charts": True})

    # ส่งคำถามไปยังโมเดล
    response = smart_df.chat(user_query)

    # แสดงผลลัพธ์
    st.subheader("ผลลัพธ์จาก AI:")
    if isinstance(response, pd.DataFrame):
        st.dataframe(response)
    elif isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg')):
        st.image(response)
    elif response is None:
        st.write("ไม่มีคำตอบกลับมา")
    else:
        st.write(response)
