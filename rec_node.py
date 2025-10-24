 #!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import time
import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------------
# 1. Speech Recognition Logic
# ----------------------------------------------------------------------
rospy.init_node(“talker”)
def recognize_speech_from_mic(duration, label):
    """Handles the actual recording and recognition."""
    pub = rospy.Publisher("/box", String, queue_size = 10)
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # Update the GUI label to show the process has started
    label.config(text="กำลังปรับแต่งระดับเสียง...")
    root.update() # Force GUI update
    
    with mic as source:
        try:
            rospy.init_node(“talker”)
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Prompt the user
            label.config(text="กรุณาพูด...")
            root.update()
            
            # Listen for audio, limited by the duration from the slider
            audio = recognizer.listen(source, timeout=duration)
            
            # Recognize speech (simple Google Web Speech API)
            text = recognizer.recognize_google(audio, language="th-TH")
            
            # Display the result
            label.config(text=f"คุณพูดว่า: {text}")

        except sr.WaitTimeoutError:
            # This occurs if the timeout is reached before any speech is detected
            label.config(text="หมดเวลา: ไม่พบการพูดในช่วงเวลาที่กำหนด")
        except sr.UnknownValueError:
            # This occurs if speech is detected but not understood
            label.config(text="ไม่สามารถเข้าใจเสียงที่พูดได้")
        except sr.RequestError:
            # This occurs if there is a network or API connection error
            label.config(text="เกิดข้อผิดพลาดในการเชื่อมต่อกับบริการ")
        except Exception as e:
            # Catch other potential errors (e.g., PyAudio issues)
            label.config(text=f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")

def start_recording():
    """Reads the duration from the slider and calls the recognition function."""
    duration = slider.get()
    recognize_speech_from_mic(duration, result_label)

# ----------------------------------------------------------------------
# 2. GUI Setup (Tkinter)
# ----------------------------------------------------------------------

# สร้าง GUI (Create GUI)
root = tk.Tk()
root.geometry("300x200")
root.title("Speech Recognition (TH)")
root.configure(bg="#f0e68c") # Yellow background

# Duration Slider
# Allows the user to select the recording time (1 to 10 seconds)
slider_label = tk.Label(root, text="ตั้งเวลาบันทึก (วินาที):", bg="#f0e68c")
slider_label.pack(pady=5)

slider = tk.Scale(root, from_=1, to=10, orient="horizontal", 
                 bg="#add8e6", length=200) # Blue background
slider.set(5) # Set default duration to 5 seconds
slider.pack()

# Record Button
record_button = ttk.Button(root, text="RECORD (กดแล้วพูด)", 
                          command=start_recording)
record_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="กด RECORD เพื่อเริ่ม", 
                        bg="#98fb98", # Green background
                        wraplength=280) 
result_label.pack(fill='x', padx=10)

# Start the GUI event loop
if __name__ == "__main__":
    root.mainloop()
