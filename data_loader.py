from preprocess_sound import preprocess_sound
from numpy.random import seed, randint
from torch.utils.data import DataLoader, Dataset, random_split
from torch.utils.data import Dataset
import torchaudio
from scipy.io import wavfile
import numpy as np
import os
import glob
import torch


class_to_idx = {
    'Orka': 0,
    'Humbak': 1,
}


class SoundDS(Dataset):
    def __init__(self, data_path, target_shape=(960, 64, 64)):  # Przykładowy docelowy kształt
        self.files = glob.glob(os.path.join(data_path, '*.wav'))
        self.target_shape = target_shape

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        sound_file = self.files[idx]
        class_id = os.path.basename(os.path.dirname(sound_file))
        class_idx = class_to_idx[class_id]

        sr, wav_data = wavfile.read(sound_file)
        wav_data = wav_data / 32768.0
        cur_spectro = preprocess_sound(wav_data, sr)

        # Dopasowanie rozmiaru spektrogramu
        cur_spectro_padded = np.zeros(self.target_shape)
        min_time_frames = min(self.target_shape[0], cur_spectro.shape[0])
        min_mel_bands = min(self.target_shape[1], cur_spectro.shape[1])

        cur_spectro_padded[:min_time_frames, :min_mel_bands] = cur_spectro[:min_time_frames, :min_mel_bands]

        return torch.tensor(cur_spectro_padded, dtype=torch.float32), torch.tensor(class_idx, dtype=torch.long)
