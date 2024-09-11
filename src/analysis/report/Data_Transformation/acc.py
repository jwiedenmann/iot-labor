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

# Correction for sensor mounting pitch angle (-11.16 degrees)
pitch_angle_rad = np.deg2rad(11.5)  # Convert +11.16 degrees (upwards) to radians
cos_pitch = np.cos(pitch_angle_rad)
sin_pitch = np.sin(pitch_angle_rad)

# Apply the correct rotation matrix to adjust the X and Z axes
df['accX_corrected'] = df['accX_smoothed'] * cos_pitch + df['accZ_smoothed'] * sin_pitch
df['accZ_corrected'] = -df['accX_smoothed'] * sin_pitch + df['accZ_smoothed'] * cos_pitch

# Calculate the pitch-corrected tilt angle using the corrected accX and accZ
df['pitch_corrected_angle'] = np.arctan2(df['accX_corrected'], df['accZ_corrected']) * (180 / np.pi)

# Plotting (This section now includes the pitch-corrected angle)
plt.figure(figsize=(14, 14))

# Acceleration X-axis (Corrected)
plt.subplot(2, 1, 1)
plt.plot(x_axis, df['accX'], label='Original accX', alpha=0.5)
plt.plot(x_axis, df['accX_smoothed'], label='Smoothed accX', linewidth=2)
plt.plot(x_axis, df['accX_corrected'], label='Corrected accX', linewidth=2, color='red')
plt.title('Acceleration X-axis Readings: Original, Smoothed, and Corrected')
plt.xlabel('Seconds' if use_seconds else 'Sample Index')
plt.ylabel('Acceleration X (mg)')
plt.legend()

# Acceleration Y-axis (unchanged)
# plt.subplot(4, 1, 2)
# plt.plot(x_axis, df['accY'], label='Original accY', alpha=0.5)
# plt.plot(x_axis, df['accY_smoothed'], label='Smoothed accY', linewidth=2)
# plt.title('Acceleration Y-axis Readings: Original vs Smoothed')
# plt.xlabel('Seconds' if use_seconds else 'Sample Index')
# plt.ylabel('Acceleration Y (mg)')
# plt.legend()

# Acceleration Z-axis (Corrected)
plt.subplot(2, 1, 2)
plt.plot(x_axis, df['accZ'], label='Original accZ', alpha=0.5)
plt.plot(x_axis, df['accZ_smoothed'], label='Smoothed accZ', linewidth=2)
plt.plot(x_axis, df['accZ_corrected'], label='Corrected accZ', linewidth=2, color='red')
plt.title('Acceleration Z-axis Readings: Original, Smoothed, and Corrected')
plt.xlabel('Seconds' if use_seconds else 'Sample Index')
plt.ylabel('Acceleration Z (mg)')
plt.legend()

# Pitch Corrected Tilt Angle (accX_corrected vs accZ_corrected for pitch correction)
# plt.subplot(4, 1, 4)
# plt.plot(x_axis, df['pitch_corrected_angle'], label='Pitch Corrected Tilt Angle', linewidth=2, color='green')
# plt.title('Pitch Corrected Tilt Angle (Corrected accX vs accZ)')
# plt.xlabel('Seconds' if use_seconds else 'Sample Index')
# plt.ylabel('Tilt Angle (degrees)')
# plt.legend()

plt.tight_layout()
plt.show()
