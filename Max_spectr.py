from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import numpy as np

from preprocess_sound import preprocess_sound

target_shape = (600, 64)

sound_file = 'Samples/Train_Humbak/Humbak63019010.wav'

sr, wav_data = wavfile.read(sound_file)
wav_data = wav_data / 32768.0
cur_spectro = preprocess_sound(wav_data, sr)
cur_spectro_padded = np.zeros(target_shape)

max_val_index = np.unravel_index(np.argmax(cur_spectro), cur_spectro.shape)

time_offset = max(0, min(max_val_index[1] - target_shape[0] // 2, cur_spectro.shape[1] - target_shape[0]))
mel_offset = max(0, min(max_val_index[2] - target_shape[1] // 2, cur_spectro.shape[2] - target_shape[1]))

cur_spectro_padded = cur_spectro[0, time_offset:time_offset + target_shape[0], mel_offset:mel_offset + target_shape[1]]

spectro_2d = cur_spectro_padded
spectro_4d = np.expand_dims(cur_spectro_padded, axis=0)

print(f"Cur_spectro: {cur_spectro.shape}")
print(f"Spectro_4d: {spectro_4d.shape}")

plt.figure(figsize=(10, 4))
plt.imshow(spectro_2d, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Intensity (dB)')
plt.xlabel('Frequency Bins')
plt.ylabel('Time Bins')
plt.title('Spectrogram Visualization')
plt.show()

print("Kształt macierzy obciętego spektogramu MEL:", spectro_2d.shape)
