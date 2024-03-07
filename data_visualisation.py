from scipy.io import wavfile
from preprocess_sound import preprocess_sound
import matplotlib.pyplot as plt
import os
import numpy as np
import torch

target_shape = (960, 64)

sound_file = 'Humbak28.wav'

sr, wav_data = wavfile.read(sound_file)
wav_data = wav_data / 32768.0
cur_spectro = preprocess_sound(wav_data, sr)
cur_spectro_padded = np.zeros(target_shape)

if cur_spectro.shape[0] > 0:
    min_time_frames = min(target_shape[0], cur_spectro.shape[1])
    min_mel_bands = min(target_shape[1], cur_spectro.shape[2])
    cur_spectro_padded[:min_time_frames, :min_mel_bands] = cur_spectro[0][:min_time_frames, :min_mel_bands]

num_rows = 1000
num_columns = len(wav_data) // num_rows
reshaped_wav_data = wav_data[:num_rows * num_columns].reshape(num_rows, num_columns)

class_id = os.path.basename(os.path.dirname(sound_file))

spectr_2d = cur_spectro[0]

plt.figure(figsize=(10, 4))
plt.imshow(spectr_2d, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Amplitude')
plt.xlabel('Samples')
plt.ylabel('Segments')
plt.title('2D Visualization of wav_data')
plt.show()

spectro_2d = cur_spectro_padded
spectro_4d = np.expand_dims(cur_spectro, axis=0)
print(spectro_4d.shape)
plt.figure(figsize=(10, 4))
plt.imshow(spectro_2d, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Intensity (dB)')
plt.xlabel('Time Bins')
plt.ylabel('Frequency Bins')
plt.title('Spectrogram Visualization')
plt.show()


print("Kształt macierzy spektogramy MEL:", spectr_2d.shape)
print("Kształt macierzy obciętego spektogramy MEL:", spectro_2d.shape)
