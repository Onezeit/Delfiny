from torch.utils.data import Dataset
import numpy as np
import os
import glob
import torch
from Generator import generator  # Upewnij się, że importujesz funkcję generator z odpowiedniego miejsca

class SoundDS(Dataset):
    def __init__(self, data_paths, target_shape=(300, 300)):
        self.files = []
        self.target_shape = target_shape

        for path in data_paths:
            for file in glob.glob(os.path.join(path, '*.wav')):
                self.files.append(file)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        sound_file = self.files[idx]
        filename = os.path.basename(sound_file).lower()

        if "orka" in filename:
            class_idx = 0
        elif "delfin" in filename:
            class_idx = 1
        else:
            class_idx = 2

        try:
            _, _, cur_spectro = generator(sound_file, self.target_shape)  # Rozpakowanie krotki
        except Exception as e:
            print(f"Problem z plikiem {filename}: {e}")
            return torch.zeros(1, *self.target_shape), torch.tensor(0)

        if cur_spectro.size == 0:
            print(f"Pusty spektrogram dla pliku: {filename}")
            return torch.zeros(1, *self.target_shape), torch.tensor(0)

        # Znajdź indeksy maksymalnej wartości w spektrogramie
        max_idx = np.unravel_index(np.argmax(cur_spectro), cur_spectro.shape)
        target_height, target_width = self.target_shape

        # Oblicz indeksy do przycięcia spektrogramu, aby zapewnić, że max wartość jest w centrum
        start_freq_idx = max(0, min(max_idx[0] - target_height // 2, cur_spectro.shape[0] - target_height))
        end_freq_idx = start_freq_idx + target_height

        start_time_idx = max(0, min(max_idx[1] - target_width // 2, cur_spectro.shape[1] - target_width))
        end_time_idx = start_time_idx + target_width

        # Przycinanie spektrogramu do pożądanego rozmiaru
        spectr_cropped = cur_spectro[start_freq_idx:end_freq_idx, start_time_idx:end_time_idx]



        # Upewnij się, że spektrogram ma odpowiedni rozmiar (wypełnianie zerami, jeśli jest mniejszy)
        spectro_height, spectro_width = spectr_cropped.shape
        padded_spectro = np.zeros(self.target_shape)
        padded_spectro[:spectro_height, :spectro_width] = spectr_cropped

        # Przekształcenie spektrogramu na odpowiedni format
        padded_spectro = np.expand_dims(padded_spectro, axis=0)

        return torch.tensor(padded_spectro, dtype=torch.float32), torch.tensor(class_idx, dtype=torch.long), filename
