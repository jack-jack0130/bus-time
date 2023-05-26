import json
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template
import time

app = Flask(__name__)



bus_no = ["272A", "272X"]
bus_dict = {bus: [] for bus in bus_no}

shuttle_timetable = ['09:00', '09:20', '09:40', '10:00', '10:20', '10:50',
               '11:10', '11:30', '11:50', '12:50', '13:10', '13:30',
               '13:50', '14:10', '14:30', '14:50', '15:10', '15:30',
               '15:50', '16:20', '16:40', '17:00', '17:20', '17:40',
               '18:00', '18:20', '18:40', '19:00', '19:15', '19:30',
               '19:45', '20:00', '20:40']

bus_time=[]
def get_bustime(x):
    url_stop = 'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/B644204AEDE7A031'

    response = requests.get(url_stop)
    ETA = response.json()



    for item in ETA['data']:
        for key, value in item.items():
            if value in x:
                for k, v in item.items():
                    if k == "eta":
                        try:
                            datetime_string = v
                            dt = datetime.fromisoformat(datetime_string)
                            trimmed_string = dt.strftime("%H:%M")
                            bus_dict[value].append(trimmed_string)
                        except TypeError as e:
                            pass

    return


def get_shuttle():
    now = datetime.now()

    # Calculate the time after 30 minutes
    time_after_30_minutes = now + timedelta(minutes=30)

    # Find times in the list within the next 30 minutes
    found_times = []
    for time_str in shuttle_timetable:
        time = datetime.strptime(time_str, '%H:%M')
        if now.time() <= time.time() <= time_after_30_minutes.time():
            found_times.append(time)

    bus_dict["shuttle"] = [dt.strftime('%H:%M') for dt in found_times]


    return

def sorting():
    print(bus_dict)


    # Collect all time values into a single list
    all_times = []
    for time_list in bus_dict.values():
        all_times.extend(time_list)

    # Sort the time values
    sorted_times = sorted(all_times, key=lambda x: datetime.strptime(x, '%H:%M'))

    # Update the bus_dict with the sorted time values for each bus
    for bus in bus_dict:
        sorted_time_list = sorted(bus_dict[bus], key=lambda x: datetime.strptime(x, '%H:%M'))
        bus_dict[bus] = sorted_time_list

    # Print the sorted time values with their corresponding bus
    for time in sorted_times:
        for bus in bus_dict:
            if time in bus_dict[bus]:
                print(f"{time} - {bus}")
                bus_time.append(f"{time} - {bus}")
                print(bus_time)


    return



@app.route('/')
def index():
    bus_time.clear()
    get_bustime(bus_no)
    get_shuttle()
    sorting()
    # for reloading , assign empty list as value of the bus_dict
    for key in bus_dict.keys():
        bus_dict[key] = []


    return render_template('bus_time.html', output=bus_time )

