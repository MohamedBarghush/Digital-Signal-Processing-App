import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk
import math
from Practical_task_1.CompareSignal import Compare_Signals

class DSPApp:
    def __init__(self, master):
        self.master = master
        master.title("DSP Application")

        # GUI Elements
        self.fs_var = DoubleVar(master, value=8000)
        self.stop_band_attenuation_var = DoubleVar(master, value=50)
        self.fc_var = DoubleVar(master, value=1500)
        self.fc2_var = DoubleVar(master, value=1500)
        self.transition_band_var = DoubleVar(master, value=500)
        self.input_signal_var = StringVar(master, value='')

        # Labels
        Label(master, text="Filter Type:").grid(row=0, column=0, sticky=W)
        Label(master, text="Sampling Frequency (FS):").grid(row=1, column=0, sticky=W)
        Label(master, text="Stop Band Attenuation:").grid(row=2, column=0, sticky=W)
        Label(master, text="Cutoff Frequency (FC):").grid(row=3, column=0, sticky=W)
        Label(master, text="Cutoff Frequency 2 (FC2 for Band):").grid(row=4, column=0, sticky=W)
        Label(master, text="Transition Band:").grid(row=5, column=0, sticky=W)
        Label(master, text="Input Signal File:").grid(row=6, column=0, sticky=W)

        # Entry fields
        filter_types = ['Low pass', 'High pass', 'Band pass', 'Band stop']
        self.filter_type_var = StringVar(master, value=filter_types[0])
        ttk.Combobox(master, textvariable=self.filter_type_var, values=filter_types).grid(row=0, column=1)
        Entry(master, textvariable=self.fs_var).grid(row=1, column=1)
        Entry(master, textvariable=self.stop_band_attenuation_var).grid(row=2, column=1)
        Entry(master, textvariable=self.fc_var).grid(row=3, column=1)
        Entry(master, textvariable=self.fc2_var).grid(row=4, column=1)
        Entry(master, textvariable=self.transition_band_var).grid(row=5, column=1)
        Button(master, command=self.load_input, text="Import").grid(row=6, column=1)

        # Buttons
        Button(master, text="Load Filter Specs", command=self.load_filter_specs).grid(row=7, column=0, columnspan=2)
        Button(master, text="Run DSP", command=self.run_dsp).grid(row=8, column=0, columnspan=2)

    def load_input (self):
        filename = filedialog.askopenfilename()
        self.input_signal_var.set(filename)

    def load_filter_specs(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            filter_specs = read_filter_specifications_from_file(file_path)
            self.filter_type_var.set(filter_specs['FilterType'])
            self.fs_var.set(int(filter_specs['FS']))
            self.stop_band_attenuation_var.set(int(filter_specs['StopBandAttenuation']))
            # self.fc_var.set(int(filter_specs['FC']))
            self.transition_band_var.set(int(filter_specs['TransitionBand']))

            # Update for Band pass and Band stop cases
            if filter_specs['FilterType'] in ['Band pass', 'Band stop']:
                self.fc2_var.set(int(filter_specs['F2']))
                self.fc_var.set(int(filter_specs['F1']))
            else:
                self.fc_var.set(int(filter_specs['FC']))

    def run_dsp(self):
        # Get values from GUI
        filter_type = self.filter_type_var.get()
        fs = self.fs_var.get()
        stop_band_attenuation = self.stop_band_attenuation_var.get()
        fc = self.fc_var.get()
        if filter_type == "Band pass" or filter_type == "Band stop":
            f1 = self.fc_var.get()
            f2 = self.fc2_var.get()
        transition_band = self.transition_band_var.get()
        input_signal_path = self.input_signal_var.get()

        # Design FIR filter
        if filter_type == "Low pass" or filter_type == "High pass":
            indices, filter_res = design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        else:
            indices, filter_res = design_fir_filter(filter_type, fs, stop_band_attenuation, 0, transition_band, f1, f2)
        plot_signal(indices, filter_res, "Filter Coefficients")
        # convolution()

        # Read input signal from file
        if input_signal_path:
            input_x = []
            input_y = []
            with open(input_signal_path, 'r') as file:
                for line in file.readlines()[3:]:
                    data = line.split()
                    input_x.append(int(data[0]))
                    input_y.append(float(data[1]))
                file.close()
            # Apply filter
            indices, filter_res = apply_filter(input_x, input_y, indices, filter_res)
            plot_signal(input_x, input_y, "Input Signal")
            plot_signal(indices, filter_res, "Filtered Signal")


        # testing stuff
        file_path = filedialog.askopenfilename()
        Compare_Signals(file_path, indices, filter_res)

        # Save coefficients to a file
        save_coefficients_to_file(list(zip(indices, filter_res)), "filter_coefficients.txt")

        # Resample signal
        M = 4
        L = 2
        # resampled_signal = resample_signal(input_signal, M, L, len(taps))
        # plot_signal(resampled_signal, f"Resampled Signal (M={M}, L={L})")

        plt.tight_layout()
        plt.show()

def round_up_to_odd(number):
    rounded_number = math.ceil(number)
    
    if rounded_number % 2 == 0:
        rounded_number += 1

    return rounded_number

def window_function(stop_band_attenuation, n, N):
    if stop_band_attenuation <= 21:     # Rectangular
        return 1
    elif stop_band_attenuation <= 44:   # Hanning
        return 0.5 + (0.5 * np.cos((2 * np.pi * n) / N))
    elif stop_band_attenuation <= 53:   # Hamming
        return 0.54 + (0.46 * np.cos((2 * np.pi * n) / N))
    elif stop_band_attenuation <= 74:   # Blackman
        return 0.42 + (0.5 * np.cos(2 * np.pi * n / (N - 1))) + 0.08 * np.cos(4 * np.pi * n / (N - 1))

def design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band, f1=None, f2=None):
    # calculate the damn N
    delta_f = transition_band / fs
    if stop_band_attenuation <= 21:     # Rectangular
        N = round_up_to_odd(0.9/delta_f)
    elif stop_band_attenuation <= 44:   # Hanning
        N = round_up_to_odd(3.1/delta_f)
    elif stop_band_attenuation <= 53:   # Hamming
        N = round_up_to_odd(3.3/delta_f)
    elif stop_band_attenuation <= 74:   # Blackman
        N = round_up_to_odd(5.5/delta_f)

    # the list to hold the filter
    h = []
    # the x values
    indices = range(-math.floor(N/2), math.floor(N/2) + 1)

    # get filter
    #   low-pass
    if filter_type == 'Low pass':
        new_fc = fc + 0.5 * transition_band
        new_fc = new_fc / fs

        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 2*new_fc
            else:
                h_d = 2*new_fc * (np.sin(n*2*np.pi*new_fc)/(n*2*np.pi*new_fc))
            h.append(h_d*w_n)
        # [print(row) for row in list(zip(indices, h))]
            
    #   high-pass
    elif filter_type == 'High pass':
        new_fc = fc - 0.5 * transition_band
        new_fc /= fs

        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 1 - 2*new_fc
            else:
                h_d = -2*new_fc * (np.sin(n*2*np.pi*new_fc)/(n*2*np.pi*new_fc))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]

    #   band-pass
    elif filter_type == 'Band pass':
        new_fc = f1 - 0.5 * transition_band
        new_fc /= fs
        new_fc2 = f2 + 0.5 * transition_band
        new_fc2 /= fs
        
        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 2*(new_fc2 - new_fc)
            else:
                h_d = 2*new_fc2*(np.sin(n*2*np.pi*new_fc2)/(n*2*np.pi*new_fc2)) - 2*new_fc*(np.sin(n*2*np.pi*new_fc)/(n*2*np.pi*new_fc))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]

    #   band-stop
    elif filter_type == 'Band stop':
        new_fc = f1 + 0.5 * transition_band
        new_fc /= fs
        new_fc2 = f2 - 0.5 * transition_band
        new_fc2 /= fs
        
        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 1-2*(new_fc2 - new_fc)
            else:
                h_d = 2*new_fc*(np.sin(n*2*np.pi*new_fc)/(n*2*np.pi*new_fc)) - 2*new_fc2*(np.sin(n*2*np.pi*new_fc2)/(n*2*np.pi*new_fc2))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]

    return indices, h

# Convolve from previous tasks
def convolution(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)
    result = []

    start_index = int(min(x_values1) + min(x_values2))
    end_index = int(max(x_values1) + max(x_values2))

    x_values = list(range(start_index, end_index + 1))

    for n in range(len1 + len2 - 1):
        sum = 0
        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                sum += y_values1[m] * y_values2[n - m]
        result.append(sum)
    return x_values, result

# applying the filters
def apply_filter(input_x, input_y, filter_x, filter_y):
    output_x, output_y = convolution(input_x, input_y, filter_x, filter_y)
    # output_signal = signal.convolve(input_signal, taps, mode='same')
    return output_x, output_y

# plotting
def plot_signal(x, y, title):
    fig, ax = plt.subplots()  # Use plt.subplots() to create both figure and axes
    
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')

def save_coefficients_to_file(coefficients, filename):
    np.savetxt(filename, coefficients, delimiter=',')

def read_filter_specifications_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    filter_specs = {}
    for line in lines:
        key, value = line.strip().split('=')
        filter_specs[key.strip()] = value.strip()

    return filter_specs

# def resample_signal(input_signal, M, L, N):
#     if M == 0 and L != 0:
#         upsampled_signal = signal.resample_poly(input_signal, L, 1)
#         return apply_filter(upsampled_signal, design_fir_filter('Low pass', 1, 60, 0.5, 0.25))

#     elif M != 0 and L == 0:
#         return apply_filter(input_signal, design_fir_filter('Low pass', 1, 60, 0.5, 0.25))

#     elif M != 0 and L != 0:
#         upsampled_signal = signal.resample_poly(input_signal, L, 1)
#         filtered_signal = apply_filter(upsampled_signal, design_fir_filter('Low pass', 1, 60, 0.5, 0.25))
#         return signal.resample_poly(filtered_signal, 1, M)

#     else:
#         raise ValueError("Invalid values for M and L")

window = Tk()
app = DSPApp(window)
def closing_cbk():
    # Shutdown procedure
    window.quit()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", closing_cbk)
window.mainloop()

