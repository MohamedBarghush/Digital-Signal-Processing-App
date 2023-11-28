import os
import subprocess
import tkinter as tk

def run_main(folder_name):
    main_path = os.path.join(folder_name, 'main.py')
    if os.path.exists(main_path):
        subprocess.Popen(['python', main_path])
    else:
        print(f"Error: {main_path} not found.")

root = tk.Tk()
root.title("Run main.py in Folders")

folders = ['Convolution', 'Derivative', 'Moving Average', "Remove DC Component", 'Shifting and Folding']

for folder in folders:
    button = tk.Button(root, text=folder, command=lambda f=folder: run_main(f), width=30, height=2)
    button.pack(pady=10, padx=10)

root.mainloop()
