from tkinter import *
from tkinter import filedialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from Task5Test import SignalSamplesAreEqual

def read_signal_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    signal_type = int(lines[0])
    n_samples = int(lines[2])

    data_lines = lines[3:]

    signal_data = []

    for line in data_lines:
        values = list(map(float, line.split()))
        signal_data.append(values)

    return signal_type, n_samples, np.array(signal_data)

def DCT(x):
    N = len(x)
    results = np.array([])

    for k in range(N):
        val = []
        for new_n in range(N):
            val.append(x[new_n] * np.cos((np.pi / (4 * N)) * (2 * new_n - 1) * (2 * k - 1)))
        results = np.append(results, np.sum(val))
    results *= np.sqrt(2 / N)

    return results

def remove_dc_component(x):
    return x - np.mean(x)




def plot_signals(time, signal, processed_signal, operation):
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    fig.set_figwidth(10)
    fig.set_figheight(6)

    ax[0].plot(time, signal)
    ax[0].set_title('Original Signal')
    ax[0].set_xlabel('Time')

    if operation == 'Remove DC Component':
        ax[1].plot(np.arange(len(processed_signal)), processed_signal)
        ax[1].set_title(f'Signal after {operation}')
        ax[1].set_xlabel('Sample Index')
    else:
        ax[1].stem(processed_signal, basefmt='C3')
        ax[1].set_title(f'Signal after {operation}')
        ax[1].set_xlabel('DCT Coefficients')

    plt.tight_layout()
    plt.show()

def save_to_file(processed_signal, num_coefficients, operation):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            if operation == 'Remove DC Component':
                for i, value in enumerate(processed_signal):
                    file.write(str(i) + " " + str(value) + "\n")
            else:
                for i in range(num_coefficients):
                    file.write("0 " + str(processed_signal[i]) + "\n")
        messagebox.showinfo("Save Coefficients", str(num_coefficients) + " coefficients after " + str(operation) + " saved successfully.")

def browse_file():
    if operation_combo_box.get():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            signal_type, n_samples, signal_data = read_signal_file(filename)
            time = signal_data[:, 0] if signal_type == 0 else np.arange(n_samples)

            if operation_combo_box.get() == "DCT":
                processed_signal = DCT(signal_data[:, 1])
            else:
                processed_signal = remove_dc_component(signal_data[:, 1])

            plot_signals(time, signal_data[:, 1], processed_signal, operation_combo_box.get())

            # Enable the input for the number of coefficients
            num_coefficients_label.config(state='normal')
            num_coefficients_text.config(state='normal')
            save_button.config(state='normal')

            # Display the number of coefficients in the GUI
            num_coefficients_text.delete(0, END)
            num_coefficients_text.insert(0, str(len(processed_signal)))

            # Save selected coefficients to a text file
            global processed_signal_global
            processed_signal_global = processed_signal


            if (operation_combo_box.get() == "Remove DC Component"):
                SignalSamplesAreEqual("DC_component_output.txt", processed_signal_global)
            else:
                 SignalSamplesAreEqual("DCT_output.txt", processed_signal_global)

    else:
        messagebox.showinfo("Select Operation", "Please select the operation before browsing the signal file.")




def start_saving():
    try:
        num_coefficients = int(num_coefficients_text.get())
        global operation
        operation = operation_combo_box.get()
        save_to_file(processed_signal_global, num_coefficients, operation)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid number.")


# GUI setup
window = Tk()
window.title("Task 5")
window.geometry("400x200")
# Style configuration
style = ttk.Style()
style.configure("TButton", padding=5, relief="flat", background="#ccc")
style.map("TButton", foreground=[('active', '#333')], background=[('active', '#ddd')])

# Combo box for choosing DCT or Remove DC Component
Label(window, text="Choose Operation:").pack()
operations = ["DCT", "Remove DC Component"]
operation_combo_box = ttk.Combobox(window, values=operations, state="readonly")
operation_combo_box.set(operations[0])
operation_combo_box.pack()

browse_button = ttk.Button(window, text="Browse Signal File", command=browse_file)
browse_button.pack(pady=10)

# Entry for user to input the number of coefficients
num_coefficients_label = Label(window, text="Number of Coefficients to Save:")
num_coefficients_label.pack()
num_coefficients_text = Entry(window, state='disabled')
num_coefficients_text.pack()

# Save button
save_button = ttk.Button(window, text="Save File", command=start_saving, state='disabled')
save_button.pack(pady=10)


window.mainloop()
