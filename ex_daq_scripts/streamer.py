# %% find device name
import nidaqmx
import nidaqmx.system
import nidaqmx.stream_readers
import numpy as np
from datetime import datetime
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt

system = nidaqmx.system.System.local()
print(system.driver_version)
for device in system.devices:
    print(device)
# check if device is exsit
model_name = "NI_9234"
device = system.devices[model_name]
device == nidaqmx.system.Device(model_name)

fs = 51200  # sampling rate
channel = 0
frame_duration = 100  # ms
frame_size = int(fs * frame_duration * 0.001)
max_channel_quantity = 4

#samps_per_frame = 100000
# task.ai_channels.add_ai_accel_chan("cDAQ1/ai" + str(channel))
# with nidaqmx.Task(new_task_name="NI9234") as task:
task = nidaqmx.Task(new_task_name='NI9234')
task.ai_channels.add_ai_accel_chan(f'{model_name}/ai{channel}')
task.timing.cfg_samp_clk_timing(rate=fs, sample_mode=AcquisitionType.CONTINUOUS)

# %%
fig, ax = plt.subplots()
xdata, ydata = [], []
(ln,) = plt.plot([], [], "ro")
# %%


#chunk = np.zeros(frame_size)
chunk = np.zeros((1, 5120))
samples = np.array([])

stream_file = open('test.csv', 'a')

task.in_stream.input_buf_size = frame_size * 100  # set buffer size


def callback(task_handle, every_n_samples_event_type,
             number_of_samples, callback_data):
    global samples
    print(datetime.now().isoformat(sep=' ', timespec='milliseconds'))
    stream_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(task.in_stream)
    stream_reader.read_many_sample(chunk)
    #chunk = task.in_stream.read(number_of_samples_per_channel=frame_size)
    print(f'Every {number_of_samples} Samples callback invoked.')
    print(chunk[0, 50], 'callback data:', callback_data)
    #chunk = task.in_stream.read(number_of_samples_per_channel=2000)
    #samples = np.append(samples, chunk)
    # print(len(samples))
    return 0
    # task.register_every_n_samples_transferred_from_buffer_event(
    #     sample_interval=frame_size, callback_method=callback)


task.register_every_n_samples_acquired_into_buffer_event(
    sample_interval=frame_size, callback_method=callback)

task.start()

#stream_reader = nidaqmx.stream_readers
# stream_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(task.in_stream)
# a = np.zeros((1,samps_per_frame))
# print(stream_reader.read_many_sample(a))
# task.close()


input('Running task. Press Enter to stop and see number of '
      'accumulated samples.\n')
task.is_task_done()
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
