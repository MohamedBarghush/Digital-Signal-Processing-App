# Hello World
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinterdnd2 import DND_FILES,  TkinterDnD
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Prepare the plot
class Plot:
    # initialize class
    def __init__(self): 
        self.setValues()

    # set all the values needed
    def setValues (self, waveType = "Sine wave", analogFrequency = 100, samplingFrequency = 200, phaseShift = 3.14, amplitude = 1, file="", duration=1):
        self.waveType = waveType
        self.samplingFrequency = samplingFrequency
        self.analogFrequency = analogFrequency
        self.phaseShift = phaseShift
        self.amplitude = amplitude
        self.file = file
        self.duration = duration

    # Draw the plot
    def drawPlot(self, drawDiscrete = False):
        new_window = Toplevel(window)
        if drawDiscrete:
            # new_dis_window = Toplevel(window)
            new_window.geometry("1200x400")
            fig,ax = plot.subplots(1, 2)
            # fig_dis, ax_dis = plot.subplots()
        else:
            new_window.geometry("600x400")
            fig,ax = plot.subplots()

        # xCon = np.linspace(0, 1, self.samplingFrequency)
        xCon = np.arange(0, self.duration, 0.001)
        xDis = np.arange(0, self.duration, 1 / self.samplingFrequency)
        # xDis = np.append(xDis, 1)
        
        if self.waveType == "Sine wave":
            title = "Sine wave representation"
            equation = "Amplitude"
            yCon = self.amplitude*np.sin(2*np.pi*self.analogFrequency*xCon + self.phaseShift)
            yDis = self.amplitude*np.sin(2*np.pi*self.analogFrequency*xDis + self.phaseShift)
            # yDis[-1] = 0
        else:
            title = "Cosine wave representation"
            equation = "Amplitude"
            yCon = self.amplitude*np.cos(2*np.pi*self.analogFrequency*xCon + self.phaseShift)
            yDis = self.amplitude*np.cos(2*np.pi*self.analogFrequency*xDis + self.phaseShift)
            # yDis[-1] = 0

        fig.set_figwidth(15)
        if drawDiscrete:
            ax[0].plot(xCon, yCon)
            ax[1].stem(xDis, yDis)
            plot.title = title
            for e in ax:
                # e.set_title(title)
                e.set_xlabel('Time (t)')
                e.set_ylabel(equation)
                e.grid(True, which='both')
        else:
            ax.plot(xCon, yCon)
            ax.set_title(title)
            ax.set_xlabel('Time (t)')
            ax.set_ylabel(equation)
            ax.grid(True, which='both')

        # ax.axhline(y=0, color='k')
        # ax.axvline(x=0, color='k')
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Read data from a file
    def drawPlotFile (self, plotType=0):
        x = np.array([])
        y = np.array([])
        try:
            with open(self.file, 'r') as file:
                file.readline()
                file.readline()
                N = file.readline()
                for i in range(0, int(N)):
                    line = file.readline()
                    line = line.split(" ")
                    x = np.append(x, float(line[0]))
                    y = np.append(y, float(line[1]))
        except FileNotFoundError:
            print("Input file not found!")
            return
        except (IndexError, ValueError):
            print("Invalid input format in the file!")
            return
        
        new_window = Toplevel(window)
        if plotType == 1:
            new_window.geometry("600x400")
            fig,ax = plot.subplots()
            ax.plot(x,y)
            ax.stem(x,y)
            ax.set_title('File Visualization')

            ax.set_xlabel('Time (t)')
            ax.set_ylabel('Amplitude')
            ax.grid(True, which='both')
            ax.axhline(y=0, color='k')
            ax.axvline(x=0, color='k')
            
        else:
            new_window.geometry("1200x400")
            fig,ax = plot.subplots(1, 2)
            ax[0].plot(x, y)
            ax[1].stem(x, y)

            ax[0].set_title('Continous Signal Visualization')
            ax[1].set_title('Discrete Signal Visualization')

            for e in ax:
                e.set_xlabel('Time (t)')
                e.set_ylabel('Amplitude')
                e.grid(True, which='both')
                e.axhline(y=0, color='k')
                e.axvline(x=0, color='k')

        fig.set_figwidth(15)

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Create the app window
window = TkinterDnD.Tk()

window.title("DSP Task 1")
window.minsize(210, 100)

# Entries Variables
waveType = StringVar(value='Sine wave')
amplitude = IntVar(value=1)
analogFrequency = IntVar(value=1)
samplingFrequency = IntVar(value=2)
phaseShift = IntVar(value=0)
file = StringVar(value="")
plotType = IntVar(value=0)
duration = IntVar(value=1)

def validate (value):
    return value >= 2*analogFrequency 

# Labels
Label(window, text="Wave Type (Sine or Cosine)").grid(row=0, column=0)
Label(window, text="Amplitude (A)").grid(row=1)
Label(window, text="Analog Frequency (F)").grid(row=2)
Label(window, text="Sampling Frequency (Fs)").grid(row=3)
Label(window, text="Phase Shift (θ)").grid(row=4)
Label(window, text="Duration (s)").grid(row=5)
Label(window, text="--------------------------------------------------------------------------").grid(row=6, columnspan=4)
Label(window, text="OR").grid(row=7, columnspan=4)
Label(window, text="--------------------------------------------------------------------------").grid(row=8, columnspan=4)
Label(window, text="Drop a file with the data here").grid(row=9)
Label(window, text="Visualization Type").grid(row=10, column=0)

# Radio Buttons
OptionMenu(window, waveType, "Sine wave", "Cosine wave").grid(row=0, column=1)
# Entries
Entry(window, text="Amplitude (A)", textvariable=amplitude).grid(row=1, column=1)
Entry(window, text="Analog Frequency (F)", textvariable=analogFrequency).grid(row=2, column=1)
Entry(window, text="Sampling Frequency (F)", textvariable=samplingFrequency).grid(row=3, column=1)
Entry(window, text="Phase Shift (θ)", textvariable=phaseShift).grid(row=4, column=1)
Entry(window, text="Duration (s)", textvariable=duration).grid(row=5, column=1)

# Button functionality that creates a plot window
def create_a_plot():
    if lb.get(0) == "":
        try:
            if samplingFrequency.get() >= 2*analogFrequency.get():
                newPlot = Plot()
                newPlot.setValues(waveType=waveType.get(), amplitude=amplitude.get(), analogFrequency=analogFrequency.get(), samplingFrequency=samplingFrequency.get(), phaseShift=phaseShift.get(), duration=duration.get())
                newPlot.drawPlot(drawDiscrete=True)
            else:
                messagebox.showerror('Python Error', 'Error: Sampling Frequency can\'t be less than twice the Analog Frequency')
        except:
            newPlot = Plot()
            newPlot.setValues(waveType=waveType.get(), amplitude=amplitude.get(), analogFrequency=analogFrequency.get(), samplingFrequency=10, phaseShift=phaseShift.get(), duration=duration.get())
            newPlot.drawPlot(drawDiscrete=False)
    else:
        newPlot = Plot()
        newPlot.setValues(file=lb.get(0))
        newPlot.drawPlotFile(plotType=plotType.get())

def clearList ():
    lb.delete(0,END)

# File Entry
lb = Listbox(window, width=20, height=3)
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: lb.insert(END, e.data))
lb.grid(row=9, column=1)
Button(window, text="Clear file data", command=clearList, height=3).grid(row=9, column=2,columnspan=2)
# Radio Buttons
Radiobutton(window, text="Split", value=0, variable=plotType).grid(row=10, column=1)
Radiobutton(window, text="On Top", value=1, variable=plotType).grid(row=10, column=2)


# Buttons
Button(window, text="Draw a plot", padx=100, pady=5, command=create_a_plot).grid(columnspan=4)

def closing_cbk():
    # Shutdown procedure
    window.quit()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", closing_cbk)
window.mainloop()
