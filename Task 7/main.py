from tkinter import *
import subprocess


# Create the main window
root = Tk()
root.title("Task 7")

def open_Correlation_file():
    subprocess.run(['python', 'Correlation.py'])
def open_Time_Analysis_file():
    subprocess.run(['python', 'Time_Analysis.py'])
def open_Template_matching_file():
    subprocess.run(['python', 'Template_Matching.py'])



task1_button = Button(root, text="Correlation", command=open_Correlation_file, width=40, height=3)
task2_button = Button(root, text="Time_Analysis", command=open_Time_Analysis_file, width=40, height=3)
task3_button = Button(root, text="Template_matching", command=open_Template_matching_file, width=40, height=3)


root.geometry("300x180")

task1_button.pack(pady=1)
task2_button.pack(pady=1)
task3_button.pack(pady=1)


root.mainloop()