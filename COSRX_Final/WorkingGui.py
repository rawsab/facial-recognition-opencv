from tkinter import *
from FaceRecognition import *
from UserManager import *
from Logger import *
from PIL import Image, ImageTk
import sys
import tkinter as tk
import cv2
import espeakng
import numpy as np
import os


def exitsystem():
    sys.exit()
    

# opens settings window to turn on/off sound
def initSettingsWin(soundOn):
    def changeSound():
        if tkBool.get():
            return True
        else:
            return False
    settingsWin = tk.Tk()
    settingsWin.resizable(False, False)
    settingsWin.title("Settings:")
    settingsWin.geometry("150x150")
    tkBool = tk.IntVar()
    if soundOn:
        tkBool.set(1)
    else:
        tkBool.set(0)
    c1 = tk.Checkbutton(settingsWin, text='Python',variable=tkBool, onvalue=1, offvalue=0, command=changeSound)


# opens window to add new user
# calls addNewUser from UserManager
def initAddUserWin():
    def getText():
        temp = e1.get()
        addUserWin.withdraw()
        addNewUser(temp)
    addUserWin = tk.Tk()
    addUserWin.resizable(False, False)
    addUserWin.title("Input name of new user:")
    addUserWin.geometry("500x150")
    l1 = tk.Label(addUserWin,text="Name")
    l1.grid(row=0, padx=(20,20), pady=(20,20))
    e1 = tk.Entry(addUserWin)
    e1.grid(row=0, column=1,padx=(20,20), pady=(20,20))
    b1 = tk.Button(addUserWin,text="Submit",command=getText)
    b1.grid(row=1, padx=(20,20), pady=(20,20))
    

def show_frames():
    # read image from camera and color correct
    ret, cv2image = cap.read()
    cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
    # run frame through facial recog.
    boxes, names = facialRecognitionLoop(cv2image, speaker, knownEncodings)
    for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(cv2image, (left, top), (right, bottom), (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(cv2image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
    # convert to tkinter compatible image and update image display
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    webcam.imgtk = imgtk
    webcam.configure(image=imgtk)
    # 10ms refresh rate for webcam display
    # no noticable difference going lower on pi
    webcam.after(30,show_frames)


# setting up the main GUI
gui = tk.Tk()
gui.resizable(False, False)
gui.title("SE101 Project")
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
x_pos = int((screen_width/2) - (1000/2))
y_pos = int((screen_height/2) - (750/2))
gui.geometry("{}x{}+{}+{}".format(1000, 750, x_pos, y_pos))


# user log side bar
logsLabel = tk.Label(text="User Logs:", font=("Helvetica", 20, 'bold', 'underline'))
logs = tk.Listbox(width=30, height=20)
scrollbar = Scrollbar(gui)
# retrieves most recent logs from db
for values in getLogs("dailyLogs"):
    logs.insert(END, values)
logs.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = logs.yview)

# webcam output
webcam = tk.Label(text="Webcam Output", fg="white", bg="black", width=400, height=400)
webcamLabel = tk.Label(text="Webcam:", font=("Helvetica", 20, 'bold', 'underline'))
# main controls
addUser = tk.Button(text="Add User",width=20, height=5, bg="gray", fg="black", command=initAddUserWin)
settings = tk.Button(text="Settings", width=20, height=5, bg="gray", fg="black", command = initSettingsWin)
authButton = tk.Button(text="Authenticate User", width=20, height=5, bg="gray", fg="black")
exitButton = tk.Button(text="Exit System", width=10, height=1, bg="gray", fg="black", command=exitsystem)

# manual positioning
logs.place(x=25, y=90)
logsLabel.place(x=25, y=55)
webcam.place(x=325, y=90)
webcamLabel.place(x=325, y=55)
settings.place(x=755, y=90)
authButton.place(x=755, y=205)
addUser.place(x=755, y=320)
exitButton.place(x=25, y=480)

# initialise camera capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)

speaker = espeakng.Speaker()
print("[INFO] Initializing camera...")
print("[INFO] Loading encodings + face detector...")
filePaths = os.listdir("/home/daniel/CosRX/FaceRecognition/CurrentVersion")
knownEncodings = []
for  filePath in filePaths:
    if filePath.endswith('.pickle'):
        data = pickle.loads(open(filePath, "rb").read())
        knownEncodings.append(data)

sound = True
# run/show gui
show_frames()
gui.mainloop()
