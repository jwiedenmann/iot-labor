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

# Define the size of the rolling window for local averaging
window_size = 3

# Apply local averaging to fill NaN values using a rolling window
for column in sensor_columns:
    df[column] = df[column].fillna(df[column].rolling(window=window_size, min_periods=1, center=True).mean())

# Adjusting the millis values for resets by iterating over them
millis_adjusted = []
offset = 0

for i in range(len(df['millis'])):
    if i > 0 and df['millis'].iloc[i] < df['millis'].iloc[i - 1]:
        offset += df['millis'].iloc[i - 1]  # Add the last value before the reset to the offset
    millis_adjusted.append(df['millis'].iloc[i] + offset)

df['millis_adjusted'] = millis_adjusted

# Convert millis to seconds for easier interpretation
df['seconds'] = df['millis_adjusted'] / 1000

# Toggle variable to choose between 'seconds' or range(len(millis)) for the x-axis
use_seconds = True  # Set this to True to use 'seconds', or False to use the index range

x_axis = df['seconds'] if use_seconds else range(len(df['millis_adjusted']))

# Apply Moving Average to reduce noise (window size can be adjusted)
smoothing_window = 10
df['accX_smoothed'] = df['accX'].rolling(window=smoothing_window, center=True).mean()
df['accY_smoothed'] = df['accY'].rolling(window=smoothing_window, center=True).mean()
df['accZ_smoothed'] = df['accZ'].rolling(window=smoothing_window, center=True).mean()

# Plotting (This section remains untouched)
plt.figure(figsize=(14, 10))

# Acceleration X-axis
plt.subplot(3, 1, 1)
plt.plot(x_axis, df['accX'], label='Original accX', alpha=0.5)
plt.plot(x_axis, df['accX_smoothed'], label='Smoothed accX', linewidth=2)
plt.title('Acceleration X-axis Readings: Original vs Smoothed')
plt.xlabel('Seconds' if use_seconds else 'Sample Index')
plt.ylabel('Acceleration X (mg)')
plt.legend()

# Acceleration Y-axis
plt.subplot(3, 1, 2)
plt.plot(x_axis, df['accY'], label='Original accY', alpha=0.5)
plt.plot(x_axis, df['accY_smoothed'], label='Smoothed accY', linewidth=2)
plt.title('Acceleration Y-axis Readings: Original vs Smoothed')
plt.xlabel('Seconds' if use_seconds else 'Sample Index')
plt.ylabel('Acceleration Y (mg)')
plt.legend()

# Acceleration Z-axis
plt.subplot(3, 1, 3)
plt.plot(x_axis, df['accZ'], label='Original accZ', alpha=0.5)
plt.plot(x_axis, df['accZ_smoothed'], label='Smoothed accZ', linewidth=2)
plt.title('Acceleration Z-axis Readings: Original vs Smoothed')
plt.xlabel('Seconds' if use_seconds else 'Sample Index')
plt.ylabel('Acceleration Z (mg)')
plt.legend()

plt.tight_layout()
plt.show()
