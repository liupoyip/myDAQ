import myDAQs
directory = '.'
file_name = 'foo.csv'
myDAQs.csv_stream_writer = myDAQs.CSVStreamWriter(directory, file_name)
myDAQs.csv_stream_writer.write_csv_on()
myDAQs.daq = myDAQs.NI9234(device_name='NI_9234', task_name='myTask')
myDAQs.daq.add_accel_channel(0)
myDAQs.daq.add_microphone_channel(1)
myDAQs.daq.set_frame_duration(50)
myDAQs.daq.set_sample_rate(12800)
myDAQs.daq.start_streaming()
myDAQs.daq.close_task()
myDAQs.csv_stream_writer.write_csv_off()
myDAQs.csv_stream_writer.close_file()
