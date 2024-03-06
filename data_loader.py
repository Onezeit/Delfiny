from preprocess_sound import preprocess_sound
from torch.utils.data import Dataset
from scipy.io import wavfile
import numpy as np
import os
import glob
import torch


class SoundDS(Dataset):
    def __init__(self, data_paths, target_shape=(960, 64)):
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
        elif "humbak" in filename:
            class_idx = 1
        else:
            class_idx = 2

        sr, wav_data = wavfile.read(sound_file)
        wav_data = wav_data / 32768.0
        cur_spectro = preprocess_sound(wav_data, sr)
        cur_spectro_padded = np.zeros(self.target_shape)
        if cur_spectro.shape[0] > 0:
            min_time_frames = min(self.target_shape[0], cur_spectro.shape[1])
            min_mel_bands = min(self.target_shape[1], cur_spectro.shape[2])
            cur_spectro_padded[:min_time_frames, :min_mel_bands] = cur_spectro[0][:min_time_frames, :min_mel_bands]

        cur_spectro_padded = np.expand_dims(cur_spectro_padded, axis=0)
        return torch.tensor(cur_spectro_padded, dtype=torch.float32), torch.tensor(class_idx, dtype=torch.long), filename
