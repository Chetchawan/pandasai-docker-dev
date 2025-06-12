import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
import os
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# ดึง API key สำหรับ Groq จาก environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

# สร้าง LLM (Large Language Model) จาก Groq
llm = ChatGroq(api_key=groq_api_key, model="llama3-8b-8192")  # เปลี่ยน model ตามที่คุณต้องการ

# สร้าง DataFrame ตัวอย่าง
data = {
    "ชื่อ": ["สมชาย", "อรทัย", "วิทยา"],
    "อายุ": [30, 25, 35],
    "อาชีพ": ["วิศวกร", "ครู", "หมอ"]
}
df = pd.DataFrame(data)

# สร้าง SmartDataframe จาก pandasai
sdf = SmartDataframe(df, config={"llm": llm})

# ตัวอย่างการถามคำถามกับข้อมูล
response = sdf.chat("ใครคือวิศวะกร?")
print(response)
