# %% find device name
import nidaqmx
import nidaqmx.system
import nidaqmx.stream_readers
import numpy as np
from datetime import datetime
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt
# %%

system = nidaqmx.system.System.local()
print(system.driver_version)
for device in system.devices:
    print(device)
# %% check if device is exsit
device = system.devices["cDAQ1Mod1"]
device == nidaqmx.system.Device("cDAQ1Mod1")

# %%
fs = 51200  # sampling rate
channel = 1
frame_duration = 100  # ms
frame_size = int(fs * frame_duration * 0.001)

# %%
fig, ax = plt.subplots()
xdata, ydata = [], []
(ln,) = plt.plot([], [], "ro")
# %%
#samps_per_frame = 100000
# task.ai_channels.add_ai_accel_chan("cDAQ1/ai" + str(channel))
# with nidaqmx.Task(new_task_name="NI9234") as task:
task = nidaqmx.Task(new_task_name="NI9234")
task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai" + str(channel))
task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=AcquisitionType.CONTINUOUS)

chunk = np.zeros(frame_size)
samples = np.array([])

stream_file = open('test.csv', 'a')


def callback(task_handle, every_n_samples_event_type,
             number_of_samples, callback_data):
    global samples
    print(datetime.now().isoformat(sep=' ', timespec='milliseconds'))

    chunk = task.in_stream.read(number_of_samples_per_channel=frame_size)
    print(f'Every {number_of_samples} Samples callback invoked.')
    #chunk = task.in_stream.read(number_of_samples_per_channel=2000)
    #samples = np.append(samples, chunk)

    # print(len(samples))
    return 0
    # task.register_every_n_samples_transferred_from_buffer_event(
    #     sample_interval=frame_size, callback_method=callback)


task.register_every_n_samples_acquired_into_buffer_event(
    sample_interval=2000, callback_method=callback)

task.start()

#stream_reader = nidaqmx.stream_readers
# stream_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(task.in_stream)
# a = np.zeros((1,samps_per_frame))
# print(stream_reader.read_many_sample(a))
# task.close()


input('Running task. Press Enter to stop and see number of '
      'accumulated samples.\n')
task.stop()
stream_file.close()
# while True:
#     current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
#     data = task.in_stream.read(number_of_samples_per_channel=samps_per_frame)
#     print(current_time)


# task
# fig, ax = plt.subplots()
# xdata, ydata = [], []
# (ln,) = plt.plot([], [], "ro")


# def init():
#     ax.set_xlim(0, 1)
#     ax.set_ylim(-0.5, 0.5)
#     return (ln,)


# def update(frame):
#     data = np.asarray(task.read(number_of_samples_per_channel=samps_per_frame))
#     xdata = np.linspace(0, 1, len(data))
#     ydata = data
#     print(len(data))

#     ln.set_data(xdata, ydata)
#     print(datetime.strftime(datetime.now(), "%Y %B %w %H:%M:%S"))
#     return (ln,)


# current_time = datetime.strftime(datetime.now(), "%Y %B %w %H:%M:%S")
# ani = FuncAnimation(fig, update, frames=1, init_func=init,
#                     blit=True, interval=duration)
# plt.show()
