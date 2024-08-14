import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = 'C:\\Users\\jwiedenmann\\source\\dhbw_projects\\iot-labor\\data\\test.csv'
df = pd.read_csv(file_path, delimiter=';')

# Define the columns to clean
sensor_columns = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ', 'temp']

# Replace values above 10000 or below -10000 with NaN using map
for column in sensor_columns:
    df[column] = df[column].map(lambda x: np.nan if x > 10000 or x < -10000 else x)

# Adjusting the millis values for resets by iterating over them
millis_adjusted = []
offset = 0

for i in range(len(df['millis'])):
    if i > 0 and df['millis'][i] < df['millis'][i - 1]:
        offset += df['millis'][i - 1]  # Add the last value before the reset to the offset
    millis_adjusted.append(df['millis'][i] + offset)

df['millis_adjusted'] = millis_adjusted

# Toggle variable to choose between 'millis_adjusted' or range(len(millis)) for the x-axis
use_millis = True  # Set this to True to use 'millis_adjusted', or False to use the index range

x_axis = df['millis_adjusted'] if use_millis else range(len(df['millis_adjusted']))

# Apply Moving Average to reduce noise (window size can be adjusted)
window_size = 20
df['gyrX_smoothed'] = df['gyrX'].rolling(window=window_size, center=True).mean()
df['gyrY_smoothed'] = df['gyrY'].rolling(window=window_size, center=True).mean()
df['gyrZ_smoothed'] = df['gyrZ'].rolling(window=window_size, center=True).mean()

plt.figure(figsize=(14, 10))

# Gyroscope X-axis
plt.subplot(3, 1, 1)
plt.plot(x_axis, df['gyrX'], label='Original gyrX', alpha=0.5)
plt.plot(x_axis, df['gyrX_smoothed'], label='Smoothed gyrX', linewidth=2)
plt.title('Gyroscope X-axis Readings: Original vs Smoothed')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope X (degrees)')
plt.legend()

# Gyroscope Y-axis
plt.subplot(3, 1, 2)
plt.plot(x_axis, df['gyrY'], label='Original gyrY', alpha=0.5)
plt.plot(x_axis, df['gyrY_smoothed'], label='Smoothed gyrY', linewidth=2)
plt.title('Gyroscope Y-axis Readings: Original vs Smoothed')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope Y (degrees)')
plt.legend()

# Gyroscope Z-axis
plt.subplot(3, 1, 3)
plt.plot(x_axis, df['gyrZ'], label='Original gyrZ', alpha=0.5)
plt.plot(x_axis, df['gyrZ_smoothed'], label='Smoothed gyrZ', linewidth=2)
plt.title('Gyroscope Z-axis Readings: Original vs Smoothed')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope Z (degrees)')
plt.legend()

plt.tight_layout()
plt.show()