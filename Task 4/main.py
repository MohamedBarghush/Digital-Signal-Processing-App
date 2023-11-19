from tkinter import *
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import math
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift

x_values = []
y_values = []
N = 0.00

polar_path = ""

def ReadFile (edit = False):
    global x_values
    x_values = []
    global y_values
    y_values = []
    global N
    global frequency_range_values
    global polar_path
    file_path = filedialog.askopenfilename()
    polar_path = file_path.split("/")[-1].rstrip("txt").strip(".")
    if file_path:
        with open(file_path, 'r') as file:
            file.readline()
            file.readline()
            N = int(file.readline())
            lines = file.readlines()
            for line in lines:
                data = line.split()
                x_values.append(float(data[0].replace("f", "")))
                y_values.append(float(data[1].replace("f", "")))
            file.close()
    if edit:
        frequency_range_values = [[x_values[i],y_values[i]] for i in range(N)]

x_test = []
y_test = []


def ReadTest ():
    global N
    global x_test
    x_test = []
    global y_test
    y_test = []
    file_path = filedialog.askopenfilename()
    if (file_path):
        with open(file_path, 'r') as file:
            file.readline()
            file.readline()
            N = int(file.readline())
            lines = file.readlines()
            for line in lines:
                data = line.split()
                x_test.append(round(float(data[0].rstrip("f")), 6))
                y_test.append(round(float(data[1].rstrip("f")), 6))
            file.close()

frequency_range_values = []
fundamental_frequency = 0.0
# sampling_frequency = 0.0

def DFT_IDFT (sampling_frequency_inner, type_of_operation):
    global x_values
    global y_values
    global N
    global x_test
    global y_test
    global frequency_range_values
    # global sampling_frequency

    ## Check the damn sampling frequency as a counter-measure to it being 0 or NULL
    try:
        sampling_frequency = sampling_frequency_inner.get()
        if sampling_frequency == 0:
            messagebox.showwarning(title="Warning", message="Sampling frequency is 0, enter a sampling frequency")
            return
    except Exception as e:
        messagebox.showwarning(title="Warning", message="Sampling frequency is NULL, enter a sampling frequency")
        return

    frequency_range_values = []
    complex_values = []
    if type_of_operation == "DFT":
        x_values = [int(x) for x in x_values]
        for k in x_values:
            values = []
            for index, Xn in enumerate(y_values):
                value = [Xn*math.cos((2.0*math.pi*k*index)/N), -Xn*math.sin((2.0*math.pi*k*index)/N)]
                # value = np.exp((-2j * math.pi * k * index)/N)
                values.append([value[0], value[1]])
                # values.append([Xn*np.real(value), Xn*np.imag(value)])
            complex_values.append(values)
            # [print(np.real(x) for x in complex_values)]
            sum_x, sum_y = [sum(x) for x in zip(*values)]
            # frequency_range_values.clear()
            amplitude = math.sqrt((pow(sum_x, 2)+pow(sum_y, 2)))
            phase_shift = math.atan2(sum_y, sum_x)

            frequency_range_values.append([amplitude, phase_shift])
    else:
        for i in range(int(N)):
            real_value = 0
            imag_value = 0
            for k in range(int(N)):
                phase = 2 * math.pi * k * i / N
                # real_value = x_values[k] * math.cos(phase)
                real_value = x_values[k] * math.cos(phase) - y_values[k] * math.sin(phase)
                # imag_value = y_values[k] * math.sin(phase)
                imag_value = y_values[k] * math.sin(phase) + x_values[k] * math.sin(phase)
                complex_values.append([real_value, imag_value])
            sum_x, sum_y = [int(sum(x)/N) for x in zip(*complex_values)]
            new_x = math.sqrt((pow(sum_x, 2)+pow(sum_y, 2)))
            new_y = math.atan2(sum_y, sum_x)
            frequency_range_values.append([new_x, new_y])
        print(frequency_range_values)
        

        # new_x, new_y = [], []
        # for i in range(len(x_values)):
        #     amp = x_values[i]
        #     pahse = y_values[i]
        #     new_x.append(amp * math.cos(pahse))
        #     new_y.append(amp * math.sin(pahse))
        # for k in new_x:
        #     values = []
        #     for index in new_y:
        #         value = np.exp((2j * math.pi * k * index)/N)
        #         values.append([np.real(value)/sampling_frequency, np.imag(value)/sampling_frequency])
        #     complex_values.append(values)
        #     # [print(np.real(x) for x in complex_values)]
        #     sum_x, sum_y = [sum(x) for x in zip(*values)]
        #     # frequency_range_values.clear()
        #     amplitude = math.sqrt((pow(sum_x, 2)+pow(sum_y, 2)))
        #     phase_shift = math.atan2(sum_y, sum_x)

        #     frequency_range_values.append([amplitude, phase_shift])
        #     print(frequency_range_values)

    
    # print(frequency_range_values)

    # [print((str(x[0])+" "+str(x[1]))) for x in frequency_range_values]

    val = SignalComapreAmplitude([round(row[0], 6) for row in frequency_range_values], x_test)
    val2 = SignalComaprePhaseShift([round(row[1], 6) for row in frequency_range_values], y_test)
    if val and val2:
        print("Congrats on both")
    else:
        print("Fuck on both or only one")

    Draw_Data(sampling_frequency, typo=type_of_operation)

    

def Save_File (new_file_name):
    global N
    global frequency_range_values

    if frequency_range_values == []:
        messagebox.showerror(title="Problem", message="No Data Daved for writing in the file, save data with the button above before saving")

    print(new_file_name)
    with open(new_file_name+".txt","w") as file:
        file.write("0\n")
        file.write("1\n")
        file.write(str(N)+"\n")
        for n in range(int(N)):
            file.write(str(frequency_range_values[n][0])+" "+str(frequency_range_values[n][1])+"\n")

    messagebox.showinfo(title="For Your Info", message="File Saved Successfully")

def Draw_Data (sampling_frequency_inner = 0, typo = "DFT"):
    global frequency_range_values
    global x_values
    global y_values
    global N

    # try:
    #     sampling_frequency = sampling_frequency_inner.get()
    #     if sampling_frequency == 0:
    #         messagebox.showwarning(title="Warning", message="Sampling frequency is 0, enter a sampling frequency")
    #         return
    # except Exception as e:
    #     messagebox.showwarning(title="Warning", message="Sampling frequency is NULL, enter a sampling frequency")
    #     return

    fundamental_frequency = (2*np.pi)/(N*(1/sampling_frequency_inner))
    x_values = [x for x in range(int(N))]
    fundamental_frequency_ranges = [fundamental_frequency*x for x in x_values]

    new_window = Toplevel(window)


    new_window.geometry("1000x600")
    fig,ax = plt.subplots(1, 2)

    ax[0].stem(fundamental_frequency_ranges, [row[0] for row in frequency_range_values])
    ax[1].stem(fundamental_frequency_ranges, [row[1] for row in frequency_range_values])

    ax[0].set_xlabel("Frequency")
    ax[0].set_ylabel("Amplitude")
    ax[1].set_xlabel("Phase Shift")
    ax[1].set_ylabel("Amplitude")

    ax[0].set_xticks(fundamental_frequency_ranges)
    ax[1].set_xticks(fundamental_frequency_ranges)

    fig.set_figwidth(10)
    fig.set_figheight(6)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def Edit_Data (index, new_x, new_y, new_file_name):
    global N
    global frequency_range_values
    try:
        index = index.get()
        if index > (N-1):
            messagebox.showerror(title="Error!!", message="Index out of range!")
            return
    except Exception as e:
        messagebox.showerror(title="Error!!", message="You need to provide index")
        return

    stopped = False
    
    try:
        new_x = float(new_x.get())
    except Exception as e:
        stopped = True
        frequency_range_values[index] = [frequency_range_values[index][0], new_y]

    try:
        new_y = float(new_y.get())
    except Exception as e:
        if not stopped:
            frequency_range_values[index] = [new_x, frequency_range_values[index][1]]
            stopped = True

    if not stopped:
        frequency_range_values[index] = [frequency_range_values[index][0], new_y]

    Save_File(new_file_name)


window = Tk()

notebook = ttk.Notebook(window)
notebook.pack(pady=10, padx=10)

############################ First tab  ################################
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='DFT')

Button(tab1, text="Upload File", command=ReadFile, width=15).grid(row=0, column=0, padx=2, pady=5)
Button(tab1, text="Upload Test", command=ReadTest, width=15).grid(row=0, column=1, padx=2, pady=5)

sampling_frequency_1 = IntVar(value=0)
Label(tab1, text="Sampling Frequency", width=20).grid(row=1, column=0, padx=2, pady=5)
Entry(tab1, textvariable=sampling_frequency_1, width=10).grid(row=1, column=1, padx=2, pady=5)

Button(tab1, text="DFT", command=lambda: DFT_IDFT(sampling_frequency_1, "DFT"), width=35).grid(row=2, columnspan=2, padx=2, pady=5)
Button(tab1, text="Save File", command=lambda: Save_File("dft_output"), width=35).grid(row=3, columnspan=2, padx=2, pady=5)

############################ Second tab ################################
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='IDFT')

Button(tab2, text="Upload File", command=ReadFile, width=15).grid(row=0, column=0, padx=2, pady=5)
Button(tab2, text="Upload Test", command=ReadTest, width=15).grid(row=0, column=1, padx=2, pady=5)

sampling_frequency_2 = IntVar(value=0)
Label(tab2, text="Sampling Frequency", width=20).grid(row=1, column=0, padx=2, pady=5)
Entry(tab2, textvariable=sampling_frequency_2, width=10).grid(row=1, column=1, padx=2, pady=5)

Button(tab2, text="IDFT", command=lambda: DFT_IDFT(sampling_frequency_2, "IDFT"), width=35).grid(row=2, columnspan=2, padx=2, pady=5)
Button(tab1, text="Save File", command=lambda: Save_File("idft_output"), width=35).grid(row=3, columnspan=2, padx=2, pady=5)

############################ Third tab  ################################
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Editing')

Button(tab3, text="Upload File", command=lambda: ReadFile(True), width=35).grid(row=0, columnspan=2, padx=2, pady=5)

entry_index = IntVar(value=0)
Label(tab3, text="Entry Index", width=20).grid(row=1, column=0, padx=2, pady=5)
Entry(tab3, textvariable=entry_index, width=10).grid(row=1, column=1, padx=2, pady=5)

entry_frequency = DoubleVar(value=0.0)
Label(tab3, text="Entry Frequency", width=20).grid(row=2, column=0, padx=2, pady=5)
Entry(tab3, textvariable=entry_frequency, width=10).grid(row=2, column=1, padx=2, pady=5)

entry_phase = DoubleVar(value=0.0)
Label(tab3, text="Entry Phase Shift", width=20).grid(row=3, column=0, padx=2, pady=5)
Entry(tab3, textvariable=entry_phase, width=10).grid(row=3, column=1, padx=2, pady=5)

sampling_frequency_3 = IntVar(value=0)
Label(tab3, text="Sampling Frequency", width=20).grid(row=4, column=0, padx=2, pady=5)
Entry(tab3, textvariable=sampling_frequency_3, width=10).grid(row=4, column=1, padx=2, pady=5)

Button(tab3, text="Edit File", command=lambda: Edit_Data(entry_index, entry_frequency, entry_phase, polar_path), width=35).grid(row=5, columnspan=2, padx=2, pady=5)
Button(tab3, text="Draw Data", command=lambda: Draw_Data(sampling_frequency_inner=sampling_frequency_3.get()), width=35).grid(row=6, columnspan=2, padx=2, pady=5)

def closing_cbk():
    # Shutdown procedure
    window.quit()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", closing_cbk)
window.mainloop()