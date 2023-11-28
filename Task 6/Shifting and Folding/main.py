from tkinter import *
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from Shift_Fold_Signal import Shift_Fold_Signal

def delay_signal(x, signal, k):
    delayed_x = [value + k for value in x]
    delayed_signal = signal[:]
    return delayed_x, delayed_signal

def advance_signal(x, signal, k):
    advanced_x = [value - k for value in x]
    advanced_signal = signal[:]
    return advanced_x, advanced_signal


def fold_signal(x, y):
    folded_x = [-value for value in reversed(x)]
    folded_y = list(reversed(y))

    return folded_x, folded_y

def open_file():

    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            x_values = []
            y_values = []

            for line in lines[3:]:
                values = line.strip().split()
                if len(values) >= 2:
                    x_values.append(float(values[0]))
                    y_values.append(float(values[1]))

            # Clear current figure
            plt.figure(figsize=(7, 10))
            plt.clf()

            plt.subplot(2, 1, 1)
            plt.scatter(x_values, y_values, label='Original Signal')
            plt.title('Original Signal')

            # Apply the selected operation
            if combo_box.get() == "Advance":
                shift_val = int(shiftedValEntry.get())
                shifted_x, shifted_signal = advance_signal(x_values, y_values, shift_val)
            elif combo_box.get() == "Delay":
                shift_val = int(shiftedValEntry.get())
                shifted_x, shifted_signal = delay_signal(x_values, y_values, shift_val)
            elif combo_box.get() == "Fold":
                shifted_x, shifted_signal = fold_signal(x_values, y_values)
                Shift_Fold_Signal("Shifting and Folding/Output_fold.txt",shifted_x,shifted_signal)

            elif combo_box.get() == "Fold with Advance":

                shift_val = int(shiftedValEntry.get())
                folded_x, folded_y = fold_signal(x_values, y_values)
                shifted_x, shifted_signal = delay_signal(folded_x, folded_y, shift_val)
                Shift_Fold_Signal("Shifting and Folding/Output_ShifFoldedby500.txt", shifted_x, shifted_signal)


            elif combo_box.get() == "Fold with Delay":
                shift_val = int(shiftedValEntry.get())
                folded_x, folded_y = fold_signal(x_values, y_values)
                shifted_x, shifted_signal = advance_signal(folded_x, folded_y, shift_val)
                Shift_Fold_Signal("Shifting and Folding/Output_ShiftFoldedby-500.txt", shifted_x, shifted_signal)

            plt.subplot(2, 1, 2)
            plt.scatter(shifted_x, shifted_signal)
            plt.title('Modified Signal')

            # plt.tight_layout()
            plt.show()

########### GUI ####################
window = Tk()
window.geometry("200x200")
# window.configure(bg="beige")
window.title("Shifting Signal")

Label(window, text="Shifted Value").pack()

shiftedValEntry = Entry(window)
shiftedValEntry.pack()

Label(window, text="Operation on Signals").pack()

signals_operations = ["Advance", "Delay", "Fold", "Fold with Advance", "Fold with Delay"]
combo_box = ttk.Combobox(window, values=signals_operations, style="TCombobox")
combo_box.pack()

browse_and_process_button = Button(window, text="Apply Operation", command=open_file)
browse_and_process_button.pack()

def closing_cbk():
    # Shutdown procedure
    window.quit()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", closing_cbk)

window.mainloop()
