import requests
import time
from datetime import datetime

def fetch_time_data():
    url = "https://yandex.com/time/sync.json?geo=213"
    response = requests.get(url)
    raw_data = response.text
    print("Raw response:", raw_data)

    try:
        data = response.json()
        timestamp = data['time'] / 1000  # Convert milliseconds to seconds
         # Извлекаем имя часовой зоны из словаря 'clocks'
        timezone_name = data.get('clocks', {}).get('213', {}).get('name', None)
    except KeyError as e:
        print(f"Error accessing JSON data: {str(e)}")
        return None, None

    # Преобразуем временную метку в "человекопонятный" формат
    human_readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print("Human-readable time:", human_readable_time)
    print("Timezone name:", timezone_name)
    
    return timestamp, timezone_name

def calculate_time_delta():
    deltas = []
    for _ in range(5):
        start_time = time.time()
        server_time, timezone_name = fetch_time_data()

        
        if server_time is None or timezone_name is None:
            print("Failed to retrieve valid data. Skipping this iteration.")
            continue
        
        end_time = time.time()

        # Вычисляем разницу во времени
        delta = (server_time - start_time) + (end_time - server_time)
        deltas.append(delta)
        print("Delta:", delta)

    if deltas:
        average_delta = sum(deltas) / len(deltas)
        print("Average Delta:", average_delta)
    else:
        print("No valid deltas were collected.")

calculate_time_delta()
