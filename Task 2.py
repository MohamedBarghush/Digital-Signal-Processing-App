import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Listbox, StringVar, END, filedialog, Entry, Radiobutton, IntVar
import os

class Plot:
    def __init__(self):
        pass

    def add_signals(self, files):
        fig, ax = plt.subplots()
        all_time, all_amplitude = [], []
        for file in files:
            # Read data from the file, ignoring the first three lines
            data = np.genfromtxt(file, skip_header=3)
            time, amplitude = data[:, 0], data[:, 1]
            all_time.append(time)
            all_amplitude.append(amplitude)
            filename = os.path.basename(file)  # Extracting the filename from the path
            ax.plot(time, amplitude, label=filename)
        result_time = all_time[0]
        result_amplitude = np.sum(all_amplitude, axis=0)
        ax.plot(result_time, result_amplitude, label='Result', linestyle='dashed')
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Addition)')
        ax.legend()
        plt.show()

    def subtract_signals(self, files):
        fig, ax = plt.subplots()
        all_time, all_amplitude = [], []
        for file in files:
            # Read data from the file, ignoring the first three lines
            data = np.genfromtxt(file, skip_header=3)
            time, amplitude = data[:, 0], data[:, 1]
            all_time.append(time)
            all_amplitude.append(amplitude)
            filename = os.path.basename(file)  # Extracting the filename from the path
            ax.plot(time, amplitude, label=filename)
        result_time = all_time[0]
        result_amplitude = all_amplitude[0] - all_amplitude[1]
        ax.plot(result_time, result_amplitude, label='Result', linestyle='dashed')
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Subtraction)')
        ax.legend()
        plt.show()

    def multiply_signal(self, file, constant):
        data = np.genfromtxt(file, skip_header=3)
        time, amplitude = data[:, 0], data[:, 1]
        filename = os.path.basename(file)  # Extracting the filename from the path
        fig, ax = plt.subplots()
        ax.plot(time, amplitude * constant, label=f"{filename} * {constant}")
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Multiplication)')
        ax.legend()
        plt.show()

    def square_signal(self, file):
        data = np.genfromtxt(file, skip_header=3)
        time, amplitude = data[:, 0], data[:, 1]
        filename = os.path.basename(file)  # Extracting the filename from the path
        fig, ax = plt.subplots()
        ax.plot(time, amplitude ** 2, label=f"{filename} squared")
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Squared)')
        ax.legend()
        plt.show()

    def shift_signal(self, file, shift_value):
        data = np.genfromtxt(file, skip_header=3)
        time, amplitude = data[:, 0], data[:, 1]
        shifted_time, shifted_amplitude = time + shift_value, amplitude
        filename = os.path.basename(file)  # Extracting the filename from the path
        fig, ax = plt.subplots()
        ax.plot(time, amplitude, label=f"{filename} (Original)")
        ax.plot(shifted_time, shifted_amplitude, label=f"{filename} (Shifted)")
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Shifted)')
        ax.legend()
        plt.show()

    def normalize_signal(self, file, norm_type):
        data = np.genfromtxt(file, skip_header=3)
        time, amplitude = data[:, 0], data[:, 1]
        filename = os.path.basename(file)  # Extracting the filename from the path
        fig, ax = plt.subplots()
        if norm_type == 0:
            normalized_amplitude = (amplitude - np.min(amplitude)) / (np.max(amplitude) - np.min(amplitude))
            ax.plot(time, normalized_amplitude, label=f"{filename} (Normalized 0 to 1)")
        elif norm_type == 1:
            normalized_amplitude = (2 * (amplitude - np.min(amplitude)) / (np.max(amplitude) - np.min(amplitude))) - 1
            ax.plot(time, normalized_amplitude, label=f"{filename} (Normalized -1 to 1)")
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Resulting Signal (Normalization)')
        ax.legend()
        plt.show()

    def accumulate_signal(self, file):
        data = np.genfromtxt(file, skip_header=3)
        time, amplitude = data[:, 0], data[:, 1]
        accumulated_amplitude = np.cumsum(amplitude)
        filename = os.path.basename(file)  # Extracting the filename from the path
        fig, ax = plt.subplots()
        ax.plot(time, accumulated_amplitude, label=f"{filename} (Accumulated)")
        ax.set_xlabel('Time (t)')
        ax.set_ylabel('Accumulated Amplitude')
        ax.set_title('Resulting Signal (Accumulation)')
        ax.legend()
        plt.show()

# Create the app window
window = Tk()
window.title("Signal Processing App")

file_labels = []

def open_file():
    file = filedialog.askopenfilename()
    if file:
        file_labels.append(file)
        lb.insert(END, os.path.basename(file))

def clear_list():
    global file_labels
    file_labels = []
    lb.delete(0, END)

def add_signals():
    plotter = Plot()
    plotter.add_signals(file_labels)

def subtract_signals():
    plotter = Plot()
    plotter.subtract_signals(file_labels)

def multiply_signal():
    constant = float(multiply_entry.get())
    if constant is not None:
        file = file_labels[0] if len(file_labels) == 1 else None
        if file:
            plotter = Plot()
            plotter.multiply_signal(file, constant)

def square_signal():
    file = file_labels[0] if len(file_labels) == 1 else None
    if file:
        plotter = Plot()
        plotter.square_signal(file)

def shift_signal():
    shift_value = float(shift_entry.get())
    if shift_value is not None:
        file = file_labels[0] if len(file_labels) == 1 else None
        if file:
            plotter = Plot()
            plotter.shift_signal(file, shift_value)

def normalize_signal():
    norm_type = norm_var.get()
    file = file_labels[0] if len(file_labels) == 1 else None
    if file:
        plotter = Plot()
        plotter.normalize_signal(file, norm_type)

def accumulate_signal():
    file = file_labels[0] if len(file_labels) == 1 else None
    if file:
        plotter = Plot()
        plotter.accumulate_signal(file)

# Button to open file
open_button = Button(window, text="Open File", command=open_file)
open_button.grid(row=0, column=0, padx=10, pady=10)

# Listbox to display selected files
lb = Listbox(window, width=40, height=10)
lb.grid(row=1, column=0, padx=10, pady=10)

# Button to clear the list of files
clear_button = Button(window, text="Clear List", command=clear_list)
clear_button.grid(row=2, column=0, padx=10, pady=10)

# Button to add signals
add_button = Button(window, text="Add Signals", command=add_signals)
add_button.grid(row=3, column=0, padx=10, pady=10)

# Button to subtract signals
subtract_button = Button(window, text="Subtract Signals", command=subtract_signals)
subtract_button.grid(row=4, column=0, padx=10, pady=10)

# Entry for multiplying signal by a constant
multiply_entry = Entry(window)
multiply_entry.grid(row=5, column=0, padx=10, pady=10)

# Button to multiply signal by a constant
multiply_button = Button(window, text="Multiply Signal", command=multiply_signal)
multiply_button.grid(row=6, column=0, padx=10, pady=10)

# Button to square the signal
square_button = Button(window, text="Square Signal", command=square_signal)
square_button.grid(row=7, column=0, padx=10, pady=10)

# Entry for shifting signal
shift_entry = Entry(window)
shift_entry.grid(row=8, column=0, padx=10, pady=10)

# Button to shift the signal
shift_button = Button(window, text="Shift Signal", command=shift_signal)
shift_button.grid(row=9, column=0, padx=10, pady=10)

# Radiobuttons for normalization type
norm_var = IntVar(value=0)
Radiobutton(window, text="0 to 1", variable=norm_var, value=0).grid(row=10, column=0, padx=10, pady=10)
Radiobutton(window, text="-1 to 1", variable=norm_var, value=1).grid(row=11, column=0, padx=10, pady=10)

# Button to normalize the signal
normalize_button = Button(window, text="Normalize Signal", command=normalize_signal)
normalize_button.grid(row=12, column=0, padx=10, pady=10)

# Button to accumulate the signal
accumulate_button = Button(window, text="Accumulate Signal", command=accumulate_signal)
accumulate_button.grid(row=13, column=0, padx=10, pady=10)

window.mainloop()
