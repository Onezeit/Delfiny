import requests
import time
import re
import os

def read_latest_txt(latest_txt_url):
    try:
        response = requests.get(latest_txt_url)
        response.raise_for_status()
        return response.text.strip()

    except Exception as e:
        print(f"Błąd: {e}")
        return None

def get_last_live_number(m3u8_url):
    try:

        response = requests.get(m3u8_url)
        response.raise_for_status()
        last_link = re.findall(r"live(\d+).ts", response.text)[-1]
        return int(last_link)

    except Exception as e:
        print(f"Błąd: {e}")
        return None

def download_live_samples(base_url, output_directory, latest_number, interval_seconds=10, max_attempts=3, keep_latest_n=10):
    try:
        os.makedirs(output_directory, exist_ok=True)
        counter = latest_number

        while True:
            url = f"{base_url}/live{counter}.ts"
            response = requests.get(url)

            if response.status_code == 200:
                with open(os.path.join(output_directory, f"live{counter}.ts"), "wb") as file:
                    file.write(response.content)
                print(f"Pobrano plik live{counter}.ts")


                # Usuń najstarsze próbki, aby zachować tylko keep_latest_n najnowszych
                files = sorted(os.listdir(output_directory), key=lambda x: int(x[4:-3]))
                if len(files) > keep_latest_n:
                    for old_file in files[:len(files) - keep_latest_n]:
                        os.remove(os.path.join(output_directory, old_file))
                        print(f"Usunięto najstarszy plik: {old_file}")
            else:
                print(f"Błąd przy pobieraniu pliku live{counter}.ts. Status code: {response.status_code}")

            counter += 1
            time.sleep(interval_seconds)

    except Exception as e:
        print(f"Błąd: {e}")






# latest_txt_url = "https://s3-us-west-2.amazonaws.com/streaming-orcasound-net/rpi_port_townsend/latest.txt"
# latest_txt_content = read_latest_txt(latest_txt_url)
#
# if latest_txt_content is not None:
#     print(f"Zawartość pliku latest.txt: {latest_txt_content}")
# else:
#     print("Nie udało się pobrać zawartości pliku latest.txt.")
#
# m3u8_url = f"https://s3-us-west-2.amazonaws.com/streaming-orcasound-net/rpi_port_townsend/hls/{latest_txt_content}/live.m3u8"
# last_live_number = get_last_live_number(m3u8_url)
#
# if last_live_number is not None:
#     print(f"Ostatni numer live: {last_live_number}")
# else:
#     print("Nie udało się pobrać ostatniego numeru live.")
#
# base_url = f"https://s3-us-west-2.amazonaws.com/streaming-orcasound-net/rpi_port_townsend/hls/{latest_txt_content}"
# output_directory = "LiveSamples"
# download_live_samples(base_url, output_directory, last_live_number)