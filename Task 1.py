import numpy as np
from tkinter import *
import matplotlib.pyplot as plot

# Prepare the plot
class Plot:
    # initialize class
    def __init__(self): 
        self.setValues()

    # set all the values needed
    def setValues (self, min = 0, max = 3, frequency = 1, phaseShift = 90, amplitude = 1):
        self.x = np.arange(min, max, 0.001)
        self.frequency = frequency
        self.phaseShift = np.deg2rad(phaseShift)
        self.amplitude = amplitude
        self.y = []
        for v in self.x:
            self.y.append(self.amplitude*np.cos(2*np.pi*self.frequency*v + self.phaseShift))

    # draw the plot (Debug)
    # def drawPlot(self):
    #     fig = plot.figure()

    #     ax = fig.add_subplot(1, 1, 1)
    #     if self.x[0] < 0:
    #         ax.spines['left'].set_position('center')
    #         ax.spines['bottom'].set_position('center')
    #         ax.spines['right'].set_color('none')
    #         ax.spines['top'].set_color('none')
    #     fig.supxlabel("Time")
    #     fig.supylabel("x(t) = A*cos(ω*t + θ)")
    #     plot.plot(self.x, self.y, label="Sine wave", c='blue')
    #     plot.grid()

    #     plot.title('Signal')
    #     plot.show()

    # Draw the plot
    def drawPlot(self):
        plot.plot(self.x, self.y)

        plot.title('Sine wave')

        plot.xlabel('Time (t)')
        plot.ylabel('x(t) = A*cos(ω*t + θ)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.axvline(x=0, color='k')
        plot.show()

# Create the app window
window = Tk()

window.title("DSP Task 1")
window.minsize(210, 100)

# Entries Variables
min = IntVar(value=0)
max = IntVar(value=3)
amplitude = IntVar(value=1)
frequency = IntVar(value=1)
phaseShift = IntVar(value=45)

# Labels
Label(window, text="Min Time").grid(row=0, column=0)
Label(window, text="Max Time").grid(row=0, column=2)
Label(window, text="Amplitude (A)").grid(row=1)
Label(window, text="Frequency (f)").grid(row=2)
Label(window, text="Phase Shift (θ)").grid(row=3)

# Entries
Entry(window, text="Min time", textvariable=min).grid(row=0, column=1)
Entry(window, text="Max time", textvariable=max).grid(row=0, column=3)
Entry(window, text="Amplitude (A)", textvariable=amplitude).grid(row=1, column=1)
Entry(window, text="Frequency (f)", textvariable=frequency).grid(row=2, column=1)
Entry(window, text="Phase Shift (θ)", textvariable=phaseShift).grid(row=3, column=1)

# Button functionality that creates a plot window
def create_a_plot():
  newPlot = Plot()
  newPlot.setValues(min=min.get(), max=max.get(), amplitude=amplitude.get(), frequency=frequency.get(), phaseShift=phaseShift.get())
  newPlot.drawPlot()
# Buttons
Button(window, text="Draw a plot", padx=100, pady=5, command=create_a_plot).grid(columnspan=4)

# Start the program loop
window.mainloop()

