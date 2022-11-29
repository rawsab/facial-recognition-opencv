import tkinter as tk
# from tkinter import *
from tkinter.ttk import *

gui = tk.Tk()

# setting up the GUI
gui.resizable(False, False)
gui.title("SE101 Project")
gui.geometry("750x500")


# centering GUI on screen
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()

x_pos = int((screen_width/2) - (750/2))
y_pos = int((screen_height/2) - (500/2))

gui.geometry("{}x{}+{}+{}".format(750, 500, x_pos, y_pos))


# adding a placeholder for the logs
logs = tk.Label(text="User logs appear here...", fg="black", bg="white", width=20, height=20)
logsLabel = tk.Label(text="User Logs:", font=("Helvetica", 20, 'bold', 'underline'))

# adding a placeholder for the webcam
webcam = tk.Label(text="Webcam Output", fg="white", bg="black", width=30, height=20)
webcamLabel = tk.Label(text="Webcam:", font=("Helvetica", 20, 'bold', 'underline'))

# adding buttons
addUser = tk.Button(text="Add User",width=20, height=5, bg="gray", fg="black")
settings = tk.Button(text="Settings", width=20, height=5, bg="gray", fg="black")
authButton = tk.Button(text="Authenticate User", width=20, height=5, bg="gray", fg="black")
exitButton = tk.Button(text="Exit System", width=10, height=1, bg="gray", fg="black")

# manual positioning
logs.place(x=25, y=90)
logsLabel.place(x=25, y=55)
webcam.place(x=225, y=90)
webcamLabel.place(x=225, y=55)
settings.place(x=515, y=90)
authButton.place(x=515, y=205)
addUser.place(x=515, y=320)
exitButton.place(x=25, y=450)


gui.mainloop()