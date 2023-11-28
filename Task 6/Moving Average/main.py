from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from comparesignal2 import SignalSamplesAreEqual


def moving_average(data, size):
    results = []

    for i in range(len(data) - size + 1):
        my_sum = sum(data[i:(i + size)])
        moving_average = my_sum / size
        results.append(moving_average)

    return results

def open_file():
    WSize = int(windowSize_entry.get())
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            x_values = []
            y_values = []

            for line in lines[3:]:
                values = line.strip().split()
                x_values.append(float(values[0]))
                y_values.append(float(values[1]))

            results = moving_average(y_values, WSize)

        testing_file_path = filedialog.askopenfilename()
        SignalSamplesAreEqual(testing_file_path, x_values, results)

        plt.figure(figsize=(8, 6))

        plt.subplot(2, 1, 1)
        plt.plot(x_values, y_values, label='Original Data')
        plt.title('Original Data')

        plt.subplot(2, 1, 2)
        plt.plot(x_values[WSize-1:], results, label=f'Moving Average (Window Size={WSize})')
        plt.title('Data After Applying Moving Average')

        plt.xlabel('X Values')
        plt.ylabel('Y Values')
        plt.legend()

        plt.tight_layout()
        plt.show()


window = Tk()
window.geometry("200x200")
window.title("Smoothing Signal - Moving Average")

windowSizeLable = Label(window, text="Window Size")
windowSizeLable.pack()
windowSize_entry = Entry(window)
windowSize_entry.pack()
upload_button_s1 = Button(window, text="Upload SIGNAL", command=open_file)
upload_button_s1.pack()

window.mainloop()
