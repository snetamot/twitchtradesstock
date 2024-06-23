import matplotlib.pyplot as plt
import numpy as np
import threading
import time

# Create a figure with subplots
fig, axs = plt.subplots(2, 2)

# Initialize data for the subplots
xdata1, ydata1 = [], []
xdata2, ydata2 = [], []
xdata3, ydata3 = [], []
xdata4, ydata4 = [], []

# Functions to initialize the subplots
def init_plot(ax, xdata, ydata, style):
    line, = ax.plot(xdata, ydata, style)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    return line


line1 = init_plot(axs[0, 0], xdata1, ydata1, 'r-')
line2 = init_plot(axs[0, 1], xdata2, ydata2, 'g-')
line3 = init_plot(axs[1, 0], xdata3, ydata3, 'b-')
line4 = init_plot(axs[1, 1], xdata4, ydata4, 'm-')

# Thread-safe function to update the plot
def update_plot(line, xdata, ydata, frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    if len(xdata) > 100:  # Keep the list to a manageable size
        xdata.pop(0)
        ydata.pop(0)
    line.set_data(xdata, ydata)
    line.axes.relim()
    line.axes.autoscale_view()

# Update functions for each subplot
def update_subplot1():
    for frame in np.linspace(0, 20 * np.pi, 400):
        update_plot(line1, xdata1, ydata1, frame)
        time.sleep(0.1)

def update_subplot2():
    for frame in np.linspace(0, 20 * np.pi, 400):
        update_plot(line2, xdata2, ydata2, frame)
        time.sleep(0.1)

def update_subplot3():
    for frame in np.linspace(0, 20 * np.pi, 400):
        update_plot(line3, xdata3, ydata3, frame)
        time.sleep(0.1)

def update_subplot4():
    for frame in np.linspace(0, 20 * np.pi, 400):
        update_plot(line4, xdata4, ydata4, frame)
        time.sleep(0.1)

# Start threads for each subplot
threads = []
threads.append(threading.Thread(target=update_subplot1))
threads.append(threading.Thread(target=update_subplot2))
threads.append(threading.Thread(target=update_subplot3))
threads.append(threading.Thread(target=update_subplot4))

for thread in threads:
    thread.start()

# Main loop to keep the plots updating
def animate():
    while True:
        plt.pause(0.1)

animate()