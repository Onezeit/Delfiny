import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd
from scipy.signal import spectrogram
import queue
import scipy

fs = 44100
chunk_size = 4096
overlap_size = int(chunk_size * 0.75)
duration = 20
data_queue = queue.Queue()

fig, ax = plt.subplots()
spectr_data = np.zeros((int(chunk_size / 2) + 1, int(fs / (chunk_size - overlap_size) * duration)))
im = ax.imshow(spectr_data, aspect='auto', origin='lower', extent=[0, duration, 0, fs/2])
plt.colorbar(im, ax=ax)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.set_title('Spectrogram pocięty')


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    data_queue.put(indata[:, 0])


def update_plot(frame):
    global spectr_data, im
    while not data_queue.empty():
        data = data_queue.get()
        f, t, Sxx = scipy.signal.spectrogram(data, fs=fs, nperseg=chunk_size, window=('tukey', 0.25))
        Sxx_log = 10 * np.log10(Sxx + 1e-10)
        spectr_data = np.roll(spectr_data, -1, axis=1)
        spectr_data[:, -1] = Sxx_log.mean(axis=1)
        im.set_data(spectr_data)
        im.set_clim(vmin=np.min(spectr_data), vmax=np.percentile(spectr_data, 95))
        plt.draw()


stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=chunk_size)
stream.start()

ani = FuncAnimation(fig, update_plot, interval=100, blit=False)

plt.show()
