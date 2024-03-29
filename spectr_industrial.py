import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np


plik_audio = 'Samples/Train_Humbak/Humbak8600802P.wav'


def generator(file):
    sr, wav_data = wavfile.read(file)
    wav_data = wav_data / 32768.0
    frequencies, times, spectr = scipy.signal.spectrogram(wav_data, fs=1.0, window=('tukey', 0.25), nperseg=None, noverlap=None, nfft=None,
                             detrend='constant', return_onesided=True, scaling='density', axis=-1, mode='psd')

    plt.figure(figsize=(10, 4))
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectr), shading='gouraud', cmap='viridis')
    plt.colorbar(label='Intensywność (dB)')
    plt.ylabel('Częstotliwość [Hz]')
    plt.xlabel('Czas [s]')
    plt.title('Spectrogram')
    plt.show()

    return frequencies, times, spectr


if __name__ == "__main__":
    generator(plik_audio)
