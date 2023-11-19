import os
import tkinter as tk
from subprocess import Popen, DEVNULL

def execute_main(folder):
    # Change directory to the selected folder
    os.chdir(folder)
    # Execute main.py using subprocess
    Popen(['python', 'main.py'], stdout=DEVNULL, stderr=DEVNULL)
    # Change directory back to the original directory
    os.chdir(original_directory)

def create_buttons():
    # Get the list of folders in the current directory that start with "Task"
    folders = [name for name in os.listdir() if os.path.isdir(name) and name.startswith("Task")]
    
    for folder in folders:
        # Create a button for each folder with padding
        button = tk.Button(window, text=folder, command=lambda f=folder: execute_main(f), width=40)
        button.pack(pady=5, padx=10)

# Initialize Tkinter window
window = tk.Tk()
window.title("DSP Tasks")

# Store the original directory
original_directory = os.getcwd()

# Create buttons dynamically based on folders starting with "Task"
create_buttons()

# Run the Tkinter event loop
window.mainloop()
