import os
import glob
from scipy.io import wavfile
import warnings


def delete_damaged_wav_files(root_dir):
    damaged_files = []
    for wav_path in glob.iglob(f'{root_dir}/**/*.wav', recursive=True):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                wavfile.read(wav_path)
                if len(w) > 0:
                    for warn in w:
                        if "Reached EOF prematurely" in str(warn.message):
                            damaged_files.append(wav_path)
                            break
            except Exception as e:
                print(f"Error reading {wav_path}: {e}")
                damaged_files.append(wav_path)

    for file in damaged_files:
        print(f"Usuwanie pliku: {file}")
        os.remove(file)


root_directory = 'Samples/Humbak'
delete_damaged_wav_files(root_directory)

print("Zakończone czystke")
