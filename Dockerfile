# ใช้ Python 3.10 เป็นฐาน
FROM python:3.10-slim

# ตั้ง working directory ใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปที่ /app
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โค้ดทั้งหมดไปที่ /app
COPY . .

# กำหนดคำสั่งรันสคริปต์ Python
CMD ["python", "app2.py"]
