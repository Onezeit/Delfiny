import os


def delete_file(folder_path, file_name):

    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Plik '{file_name}' został pomyślnie usunięty.")
        except Exception as e:
            print(f"Nie można usunąć pliku '{file_name}'. Błąd: {e}")
    else:
        print(f"Plik '{file_name}' nie istnieje w folderze '{folder_path}'.")


folder_path = 'Samples/Train_Orka'
file_name = 'orka9750300s.wav'

delete_file(folder_path, file_name)
