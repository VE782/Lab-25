#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import time
import tkinter as tk
from tkinter import ttk

def recognize_speech_from_mic(duration, label):
 recognizer = sr.Recognizer()
 mic = sr.Microphone()
 with mic as source:
  label.config(text="กำลังปรับแต่งระดับเสียง...")
  recognizer.adjust_for_ambient_noise(source, duration=1)
  label.config(text="กรุณาพูด...")
  audio = recognizer.listen(source, timeout=duration)
 try:
  text = recognizer.recognize_google(audio, language="th-TH")
  label.config(text=f"คุณพูดว่า: {text}")
  pub.publish(text)
 except sr.UnknownValueError:
  label.config(text="ไม่สามารถเข้าใจเสียงที่พูดได้")
 except sr.RequestError:
  label.config(text="เกิดข้อผิดพลาดในการเชื่อมต่อ")
def start_recording():
 duration = slider.get()
 recognize_speech_from_mic(duration, result_label)
# Initalize ROS node
rospy.init_node('talker',anonymous=True)
pub = rospy.Publisher('/box', String, queue_size=10)
# สร้าง GUI
root = tk.Tk()
root.geometry("250x150")
root.title("Speech Recognition")
root.configure(bg="#f0e68c")
slider = tk.Scale(root, from_=1, to=10, orient="horizontal", 
bg="#add8e6")
slider.pack()
record_button = ttk.Button(root, text="RECORD", 
command=start_recording)
record_button.pack()
 
result_label = tk.Label(root, text="", bg="#98fb98")
result_label.pack()
 
root.mainloop()
