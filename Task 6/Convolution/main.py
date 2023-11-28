from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from ConvTest import ConvTest
x_values = result=[]
x_values1 = []
y_values1 = []
x_values2 = []
y_values2 = []

def apply_test(x_values, y_values):
    ConvTest(x_values, y_values)


def convolution(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

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



def open_file1():
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[3:]:
                values = line.strip().split()
                x_values1.append(float(values[0])) 
                y_values1.append(float(values[1])) 




def open_file2():
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[3:]:
                values = line.strip().split()
                x_value = float(values[0]) 
                y_value = float(values[1]) 
                x_values2.append(x_value)  
                y_values2.append(y_value)  




def perform_conv():
    x_values, result = convolution(x_values1, y_values1, x_values2, y_values2)
    apply_test(x_values, result)
    print(x_values,"\nresults:\n", result)
    plot_convolution(x_values1, y_values1, x_values2, y_values2, x_values, result)


def plot_convolution(x_values1, y_values1, x_values2, y_values2, x_result, result):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(x_values1, y_values1, label='Signal 1')
    plt.title('Signal 1')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(x_values2, y_values2, label='Signal 2')
    plt.title('Signal 2')
    plt.legend()

    # print(result)
    plt.subplot(3, 1, 3)
    plt.plot(x_result, result, label='Convolution Result', color='red')
    plt.title('Convolution Result')
    plt.legend()

    plt.show()


# GUI
root = Tk()
root.geometry("200x100")
root.title("Convolution Of Two Signals")

upload_button_s1 = Button(root, text="Upload SIGNAL - 1", command=open_file1, width=20, pady=2)
upload_button_s1.pack()

upload_button_s2 = Button(root, text="Upload SIGNAL - 2", command=open_file2, width=20, pady=2)
upload_button_s2.pack()

convolution_button = Button(root, text="Perform Convolution", command=perform_conv, width=20, pady=2)
convolution_button.pack()

root.mainloop()
