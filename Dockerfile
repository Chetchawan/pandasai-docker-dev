# ใช้ Python 3.10 เป็น base image
FROM python:3.10-slim

# ปิด interactive prompts ในระหว่างติดตั้ง
ENV DEBIAN_FRONTEND=noninteractive

# ติดตั้ง dependencies ที่จำเป็นสำหรับ Streamlit และระบบเสียง (ถ้ามีใน requirements)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory ใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปที่ /app
COPY requirements.txt .

# ติดตั้ง Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดทั้งหมดไปที่ /app
COPY . .

# เปิดพอร์ตสำหรับ Streamlit
EXPOSE 8501

# รันแอป Streamlit
CMD ["streamlit", "run", "ai_webapp.py", "--server.port=8501", "--server.address=0.0.0.0"]
