# %% find device name
import os
import pathlib
import pprint
import nidaqmx
import nidaqmx.system
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime


def get_script_directory():
    directory = str(pathlib.Path(__file__).parent.resolve())
    directory = directory.replace(os.sep, "/") + "/"
    return directory


# %%
dir_script = get_script_directory()  # script directory
os.chdir(dir_script)

# %%
system = nidaqmx.system.System.local()
print(system.driver_version)
for device in system.devices:
    print(device)

# %% check if device is exsit
device = system.devices["cDAQ1Mod1"]
device == nidaqmx.system.Device("cDAQ1Mod1")
# %%
pp = pprint.PrettyPrinter(indent=5)
fs = 12800  # sampling rate
channel = 2
duration = 200  # ms
task = nidaqmx.Task()
samps_per_frame = int(fs * duration * 0.001)
# task.ai_channels.add_ai_accel_chan("cDAQ1/ai" + str(channel))
task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai" + str(channel))
task.timing.cfg_samp_clk_timing(fs, samps_per_chan=samps_per_frame)
# %%
fig, ax = plt.subplots()
xdata, ydata = [], []
(ln,) = plt.plot([], [], "ro")


def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 0.5)
    return (ln,)


def update(frame):
    data = task.read(number_of_samples_per_channel=samps_per_frame)

    xdata = np.linspace(0, 1, len(data))
    ydata = data
    print(len(data))

    ln.set_data(xdata, ydata)
    print(datetime.now().isoformat(sep=' ', timespec='milliseconds'))
    return (ln,)


current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
ani = FuncAnimation(fig, update, frames=1, init_func=init,
                    blit=True, interval=200)
plt.show()
