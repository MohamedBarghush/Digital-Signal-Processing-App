import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

def read_signal_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    data_lines = lines[3:]

    signal_data = []

    for line in data_lines:
        values = list(map(float, line.strip().split()))
        signal_data.append(values)

    return np.array(signal_data)

def cross_correlation(x1, x2):
    N = len(x1)
    results = []

    for n in range(N+len(x2)-1):
        sum = 0
        for j in range(N):
            if n - j >= 0 and n - j < len(x2):
                sum += x1[j] * x2[(j-n)]
        results.append(((1/N)*sum))

    return results


def time_delay_analysis(x1, x2, sampling_period):
    cross_corr_result = cross_correlation(x1, x2)

    max_corr_index = np.argmax(np.abs(cross_corr_result))
    lag = max_corr_index - (len(x1) - 1)
    time_delay = lag * (1/sampling_period)

    return cross_corr_result, lag, time_delay


def plot_signals_and_correlation(signal1, signal2, corr_result, lag):
    plt.subplot(3, 1, 1)
    plt.plot(signal1, label='Signal 1')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(signal2, label='Signal 2')
    plt.legend()

    time_lags = np.arange(-len(signal1) + 1, len(signal2))
    plt.subplot(3, 1, 3)
    plt.plot(time_lags, corr_result, label='Cross-Correlation')
    plt.axvline(x=lag, color='r', linestyle='--', label='Max Correlation Lag')
    plt.legend()

    plt.show()

def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)

def process_files(file_path_var1, file_path_var2, sampling_period_var):
    signal_data1 = read_signal_file(file_path_var1.get())
    signal_data2 = read_signal_file(file_path_var2.get())

    samples_signal1 = signal_data1[:, 1]
    samples_signal2 = signal_data2[:, 1]

    # sampling_period = 1

    try:
        sampling_period = float(sampling_period_var.get())
    except Exception as e:
        messagebox.showerror("ERROR!!!!", "Enter a sampling period, the default is 1 which is what I set in the code")
        return

    corr_result, lag, time_delay = time_delay_analysis(samples_signal1, samples_signal2, sampling_period)

    print(f"Lag: {abs(lag)}")
    print(f"Time Delay: {time_delay} seconds")

    plot_signals_and_correlation(samples_signal1, samples_signal2, corr_result, lag)

def create_gui():
    root = tk.Tk()
    root.title("Time Delay Analysis with Cross-Correlation")
    root.geometry("500x200")

    file_path_var1 = tk.StringVar()
    file_path_var2 = tk.StringVar()
    sampling_period_var = tk.StringVar()

    file_frame = tk.Frame(root)
    file_frame.pack()

    file_label1 = tk.Label(file_frame, text="Choose Signal File 1:")
    file_label1.grid(row=0, column=0)

    file_entry1 = tk.Entry(file_frame, textvariable=file_path_var1, state='disabled', width=20)
    file_entry1.grid(row=0, column=1)

    file_button1 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var1), width=20, height=1)
    file_button1.grid(row=0, column=2)

    file_label2 = tk.Label(file_frame, text="Choose Signal File 2:", width=20, height=5)
    file_label2.grid(row=1, column=0)

    file_entry2 = tk.Entry(file_frame, textvariable=file_path_var2, state='disabled', width=20)
    file_entry2.grid(row=1, column=1)

    file_button2 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var2), width=20, height=1)
    file_button2.grid(row=1, column=2)

    sampling_label = tk.Label(file_frame, text="Enter Sampling Period:")
    sampling_label.grid(row=2, column=0)

    sampling_entry = tk.Entry(file_frame, textvariable=sampling_period_var, width=20)
    sampling_entry.grid(row=2, column=1)

    process_button = tk.Button(root, text="Process Signals", command=lambda: process_files(file_path_var1, file_path_var2, sampling_period_var), width=20, height=3)
    process_button.pack(pady=10)

    root.mainloop()

# Run the GUI
create_gui()
