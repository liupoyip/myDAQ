import os

import numpy as np
import pandas as pd


output_data = {'ch0_vibration': None,
               'ch1_sound': None,
               'label': None}
df_output = pd.DataFrame(columns=['ch0_vibration', 'ch1_sound', 'label'])
labels = list()
data_len = 6400
for path in os.listdir('.'):
    if os.path.isdir(path):
        labels.append(path)
print(labels)

for label in labels:
    for i in range(30):
        sig = np.load(f'./{label}/{i}.npy')

    label_store = list()
    for j in range(data_len):
        label_store.append(label)

    output_data['label'] = label
    output_data['ch0_vibration'] = sig[:, 0]
    output_data['ch1_sound'] = sig[:, 1]

    df = pd.DataFrame(output_data)

    df_output = pd.concat((df_output, df))

df_output.to_csv('./combine_data.csv', index=0)
