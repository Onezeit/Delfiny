import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

plik_audio = 'Samples/Train_Delfin/Delfin5801300D.wav'
target_shape = (300, 300)


def generator(file, target_shape):
    sr, wav_data = wavfile.read(file)
    frequencies, times, spectr = scipy.signal.spectrogram(wav_data, fs=sr, window=('tukey', 0.25))

    max_idx = np.unravel_index(np.argmax(spectr), spectr.shape)

    start_freq_idx = max(0, max_idx[0] - target_shape[0] // 2)
    end_freq_idx = min(spectr.shape[0], start_freq_idx + target_shape[0])

    start_time_idx = max(0, max_idx[1] - target_shape[1] // 2)
    end_time_idx = min(spectr.shape[1], start_time_idx + target_shape[1])

    spectr_cropped = spectr[start_freq_idx:end_freq_idx, start_time_idx:end_time_idx]
    times_cropped = times[start_time_idx:end_time_idx]
    frequencies_cropped = frequencies[start_freq_idx:end_freq_idx]

    plt.figure(figsize=(10, 4))
    plt.pcolormesh(times_cropped, frequencies_cropped, 10 * np.log10(spectr_cropped), shading='gouraud', cmap='viridis')
    plt.colorbar(label='Intensywność (dB)')
    plt.ylabel('Częstotliwość [Hz]')
    plt.xlabel('Czas [s]')
    plt.title('Spectrogram pocięty')
    plt.show()


if __name__ == "__main__":
    generator(plik_audio, target_shape)
