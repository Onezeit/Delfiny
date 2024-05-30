import numpy as np
from scipy.signal import spectrogram
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

def generator(file, target_shape):
    sr, wav_data = wavfile.read(file)

    # Jeśli plik jest stereo, zamień na mono
    if len(wav_data.shape) > 1:
        wav_data = wav_data.mean(axis=1)

    frequencies, times, spectr = spectrogram(wav_data, fs=sr, window='hann', nperseg=1024, noverlap=512)

    # Znajdź indeksy maksymalnej wartości w spektrogramie
    max_idx = np.unravel_index(np.argmax(spectr), spectr.shape)

    # Oblicz indeksy do przycięcia spektrogramu
    start_freq_idx = max(0, max_idx[0] - target_shape[0] // 2)
    end_freq_idx = min(spectr.shape[0], start_freq_idx + target_shape[0])

    start_time_idx = max(0, max_idx[1] - target_shape[1] // 2)
    end_time_idx = min(spectr.shape[1], start_time_idx + target_shape[1])

    # Przytnij spektrogram do pożądanego rozmiaru
    spectr_cropped = spectr[start_freq_idx:end_freq_idx, start_time_idx:end_time_idx]

    # Normalizacja spektrogramu
    spectr_cropped = (spectr_cropped - np.min(spectr_cropped)) / (np.max(spectr_cropped) - np.min(spectr_cropped))

    return frequencies[start_freq_idx:end_freq_idx], times[start_time_idx:end_time_idx], spectr_cropped
