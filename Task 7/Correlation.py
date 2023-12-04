from tkinter import *
from tkinter import filedialog
import numpy as np
import math
import matplotlib.pyplot as plt
from corr_test import Compare_Signals

def cross_correlation(x1, x2):
    N = len(x1)
    results = []

    for n in range(N):
        sum = 0
        for j in range(N):
            sum += x1[j]*x2[(j+n) % N]
        results.append(((1/N)*sum))

    return results

def normalize_correlation(x1,x2,corr):
    N = len(x1)
    results = []
    for n in range(N):
        n1_sum = 0
        n2_sum = 0
        for j in range(N):
            n1_sum += x1[j]**2
            n2_sum += x2[j]**2
        results.append(corr[n] / ((1/N)*math.sqrt(n1_sum*n2_sum)))

    return results


def read_signal_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    data_lines = lines[3:]

    signal_data = []

    for line in data_lines:
        values = list(map(float, line.strip().split()))
        signal_data.append(values)

    return np.array(signal_data)

def process_files(file_path1, file_path2):
    signal_data1 = read_signal_file(file_path1)
    signal_data2 = read_signal_file(file_path2)

    samples_signal1 = signal_data1[:, 1]
    samples_signal2 = signal_data2[:, 1]

    corr_result = cross_correlation(samples_signal1, samples_signal2)
    normalized_corr_result = normalize_correlation(samples_signal1, samples_signal2, corr_result)
    indices = []

    print("Normalized Cross-Correlation Result:")
    for i, value in enumerate(normalized_corr_result):
        indices.append(i)
        print(i, value)

    Compare_Signals("Point1 Correlation\CorrOutput.txt", indices, normalized_corr_result)

    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(signal_data1[:, 0], samples_signal1, label='Signal 1')
    plt.title('Signal 1')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(signal_data2[:, 0], samples_signal2, label='Signal 2')
    plt.title('Signal 2')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(indices, normalized_corr_result, label='Normalized Cross-Correlation')
    plt.title('Normalized Cross-Correlation Result')
    plt.xlabel('Index')
    plt.ylabel('Correlation Value')
    plt.legend()

    plt.tight_layout()
    plt.show()


# GUI setup
def create_gui():
    root = Tk()
    root.title("Normalized Cross-Correlation Processor")
    root.geometry("300x100")

    file_path_var1 = StringVar()
    file_path_var2 = StringVar()

    file_frame = Frame(root)
    file_frame.pack()

    file_label1 = Label(file_frame, text="Signal File 1:")
    file_label1.grid(row=0, column=0)

    file_entry1 = Entry(file_frame, textvariable=file_path_var1, state='disabled')
    file_entry1.grid(row=0, column=1)

    file_button1 = Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var1))
    file_button1.grid(row=0, column=2)

    file_label2 = Label(file_frame, text="Signal File 2:")
    file_label2.grid(row=1, column=0)

    file_entry2 = Entry(file_frame, textvariable=file_path_var2, state='disabled')
    file_entry2.grid(row=1, column=1)

    file_button2 = Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var2))
    file_button2.grid(row=1, column=2)

    process_button = Button(root, text="Process Signals",
                               command=lambda: process_files(file_path_var1.get(), file_path_var2.get()))
    process_button.pack(pady=10)

    root.mainloop()


def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)


# Run the GUI
create_gui()
