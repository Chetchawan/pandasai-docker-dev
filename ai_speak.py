import streamlit as st
import pyaudio
import wave
import speech_recognition as sr
import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
import os
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv()

# Function to record audio
def record_audio(filename, duration=5, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    st.write("Recording...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # st.write("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to convert audio to text
def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        # st.write("Converting audio to text...")
        text = recognizer.recognize_google(audio_data, language="th-TH")
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Streamlit UI
st.title("Analytica-X AI")

# Upload CSV Section
uploaded_file = st.file_uploader("อัพโหลดไฟล์ตรงนี้เด้อ ตอนนี้ได้แต่ CSV อันอื่นยังไม่ทำ", type=["csv"])
if uploaded_file is not None:
    # Use SmartDataframe instead of pd.DataFrame
    data = pd.read_csv(uploaded_file)
    st.write("CSV File Contents:")

# Audio Recording Section
if st.button("ป้อนคำสั่งโดยใช้เสียงตรงนี้นะจ๊ะ !!!"):
    OUTPUT_FILENAME = "output.wav"
    RECORD_SECONDS = 8
    record_audio(OUTPUT_FILENAME, RECORD_SECONDS)

    text = audio_to_text(OUTPUT_FILENAME)
    st.write("Recognized Text:")
    st.write(text)

    # If CSV is uploaded, use PandasAI with ChatGroq
    if uploaded_file is not None:
        # Initialize ChatGroq with the specified model and API key
        groq_api_key = os.getenv('GROQ_API_KEY')
        llm = ChatGroq(model_name='llama-3.1-70b-versatile', api_key=groq_api_key)
        smart_df = SmartDataframe(data, config={'llm': llm
                               ,"save_charts": True})

        # # Customize prompt if needed
        # custom_prompt = "Analyze the following data based on the question: "

        # Run the model with the user query and custom prompt
        response = smart_df.chat(text)
        
        # Handle the response based on its type
        if isinstance(response, pd.DataFrame):
            st.dataframe(response)
        elif response is None:
            st.write("No response received.")
        elif isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg')):
            st.image(response)
        else:
            st.write(response)