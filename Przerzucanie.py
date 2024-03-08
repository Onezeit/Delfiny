from scipy.io import wavfile
import os
import shutil


def move_files_longer_than_n_seconds(source_folder, target_folder, n):
    total_files = 0
    files_longer_than_n_seconds = 0
    files_moved = []

    for filename in os.listdir(source_folder):
        if filename.endswith('.wav'):
            file_path = os.path.join(source_folder, filename)
            try:
                sr, data = wavfile.read(file_path)
                duration = len(data) / sr
                if duration > n:
                    files_longer_than_n_seconds += 1
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    files_moved.append(filename)
            except Exception as e:
                print(f"Problem z plikiem {filename}: {e}")
            total_files += 1

    print(f"Wszystkich plików: {total_files}")
    print(f"Pliki dłuższe niż {n} sekund: {files_longer_than_n_seconds}")
    if files_moved:
        print("Pliki usunięte:")
        for file in files_moved:
            print(file)
    else:
        print("Żadne pliki nie zostały przemieszczone.")


source_folder = 'Samples/Humbak_test'
target_folder = 'Samples/Train_Orka'
n = 3

move_files_longer_than_n_seconds(source_folder, target_folder, n)

user_input = input(f"Czy chcesz przerzucić pliki dłuższe niż {n} sekund do folderu {target_folder} (tak/nie): ")
if user_input.lower() == "tak":
    move_files_longer_than_n_seconds(source_folder, target_folder, n)
