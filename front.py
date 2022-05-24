from tkinter import *
import os
from tkinter import messagebox
window = Tk()

l = Label(window, text="STUDENT HONESTY CHECK")
l.config(font=("Ariel", 30, "bold", "italic"))
l.pack()

l2 = Label(window, text="AI MODULES")
l2.config(font=("Ariel", 30, "bold", "italic"))
l2.pack()

#Function Definitions
def facial_spoofing():
    os.system('python eye_tracker.py')
    messagebox.showinfo(title="Action Completed", message="Facial Spoofing Check has completed")
def facial_recognition():
    os.system('python AttendanceProject.py')
    messagebox.showinfo(title="Action Completed", message="Attendance has been added to the csv file")
def object_detection():
    os.system('python person_and_phone.py')
    messagebox.showinfo(title="Action Completed", message="Object Detection Check has completed")
def plag_check():
    os.system('python main.py')
    messagebox.showinfo(title="Action Completed", message="Data has been stored to DB")

btn1 = Button(window, text="FACIAL SPOOFING", height=3, width=50, fg='blue', command =facial_spoofing)
btn1.place(x=500, y=200)
btn2 = Button(window, text="FACIAL RECOGNITION", height=3, width=50, fg='blue', command =facial_recognition)
btn2.place(x=500, y=280)
btn3 = Button(window, text="OBJECT DETECTION", height=3, width=50, fg='blue', command =object_detection)
btn3.place(x=500, y=360)
btn4 = Button(window, text=".PDF DETECTION AND PLAGIARISM CHECKER", height=3, width=50, fg='blue', command =plag_check)
btn4.place(x=500, y=440)

window.title('AI MODULES')
window.geometry("1500x1100")
window.mainloop()
