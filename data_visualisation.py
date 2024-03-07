from scipy.io import wavfile
from preprocess_sound import preprocess_sound
import matplotlib.pyplot as plt
import os
import numpy as np
import torch

target_shape = (960, 64)

sound_file = 'Samples/Orka_test/6412400I.wav'

sr, wav_data = wavfile.read(sound_file)
wav_data = wav_data / 32768.0
cur_spectro = preprocess_sound(wav_data, sr)

print(f"Cur_spectro: {cur_spectro.shape}")
cur_spectro_padded = np.zeros(target_shape)
print(f"cur_spectro_padded: {cur_spectro_padded.shape}")

min_time_frames = min(target_shape[0], cur_spectro.shape[1])
min_mel_bands = min(target_shape[1], cur_spectro.shape[2])
cur_spectro_padded[:min_time_frames, :min_mel_bands] = cur_spectro[0][:min_time_frames, :min_mel_bands]

num_rows = 1000
num_columns = len(wav_data) // num_rows
reshaped_wav_data = wav_data[:num_rows * num_columns].reshape(num_rows, num_columns)

class_id = os.path.basename(os.path.dirname(sound_file))

spectro_2d = cur_spectro_padded
spectro_4d = np.expand_dims(cur_spectro_padded, axis=0)

print(f"Cur_spectro: {cur_spectro.shape}")
print(f"Spectro_4d: {spectro_4d.shape}")

plt.figure(figsize=(10, 4))
plt.imshow(cur_spectro_padded, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Intensity (dB)')
plt.xlabel('Time Bins')
plt.ylabel('Frequency Bins')
plt.title('Spectrogram Visualization')
plt.show()

print("Kształt macierzy obciętego spektogramy MEL:", spectro_2d.shape)
