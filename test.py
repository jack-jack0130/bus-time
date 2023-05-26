from datetime import datetime, timedelta

# List of times
time_list = ['10:00', '12:30', '15:15', '18:20', '18:30', '20:45']

# Get the current time
now = datetime.now()

# Calculate the time after 30 minutes
time_after_30_minutes = now + timedelta(minutes=30)

# Find times in the list within the next 30 minutes
found_times = []
for time_str in time_list:
    time = datetime.strptime(time_str, '%H:%M')
    if now.time() <= time.time() <= time_after_30_minutes.time():
        found_times.append(time)

# Print the found times if available
if found_times:
    print("Found times within the next 30 minutes:")
    for i, found_time in enumerate(found_times):
        print(f"found_time_{i+1}: {found_time.strftime('%H:%M')}")
else:
    print("No times found within the next 30 minutes")
print(found_times)