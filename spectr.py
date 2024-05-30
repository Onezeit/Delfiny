import numpy as np
from scipy.signal import spectrogram
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from Generator import generator

plik_audio = 'Samples/Train_Orka/Orka97692015.wav'
target_shape = (300, 300)  # Możesz dostosować do swoich wymagań

if __name__ == "__main__":
    frequencies, times, spectrogram_data = generator(plik_audio, target_shape)

    # Rysowanie spektrogramu
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram_data), shading='gouraud', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.show()
