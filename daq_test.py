import myDAQs
directory = '.'
file_name = 'foo.csv'
myDAQs.csv_stream_writer = myDAQs.CSVStreamWriter(directory, file_name)
myDAQs.csv_stream_writer.write_csv_on()
myDAQs.niDAQ = myDAQs.NI9234(device_name='NI_9234', task_name='myTask')
myDAQs.niDAQ.add_accel_channel(0)
myDAQs.niDAQ.add_microphone_channel(1)
myDAQs.niDAQ.set_frame_duration(50)
myDAQs.niDAQ.set_sample_rate(12800)
myDAQs.niDAQ.start_streaming()
myDAQs.niDAQ.close_task()
myDAQs.csv_stream_writer.write_csv_off()
myDAQs.csv_stream_writer.close_file()
