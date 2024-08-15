import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        offset += df['millis'].iloc[i - 1]  # Use .iloc to ensure proper indexing
    millis_adjusted.append(df['millis'].iloc[i] + offset)

df['millis_adjusted'] = millis_adjusted

# Toggle variable to choose between 'millis_adjusted' or range(len(millis)) for the x-axis
use_millis = True  # Set this to True to use 'millis_adjusted', or False to use the index range

x_axis = df['millis_adjusted'] if use_millis else range(len(df['millis_adjusted']))

# Apply Moving Average to reduce noise (window size can be adjusted)
window_size = 20
df['gyrZ_smoothed'] = df['gyrZ'].rolling(window=window_size, center=True).mean()

# Calculate time differences
df['time_seconds'] = df['millis_adjusted'] / 1000
df['delta_time'] = np.diff(df['time_seconds'], prepend=df['time_seconds'].iloc[0])

# Recalculate the tilt angle using atan2(accY, accZ)
df['acc_angle_corrected_alt'] = np.arctan2(df['accY'], df['accZ']) * 180 / np.pi

# Initialize variables for complementary filter
alpha = 0.98  # Filter coefficient (adjust this as needed)

# Avoid chained assignment by assigning with .loc[]
df.loc[0, 'comp_angle'] = df['acc_angle_corrected_alt'].iloc[0]

# Apply complementary filter using gyrZ and the alternative corrected accelerometer angle
for i in range(1, len(df)):
    df.loc[i, 'comp_angle'] = (alpha * (df['comp_angle'].iloc[i-1] + df['gyrZ'].iloc[i] * df['delta_time'].iloc[i])) + ((1 - alpha) * df['acc_angle_corrected_alt'].iloc[i])

# Apply complementary filter for smoothed data
df.loc[0, 'comp_angle_smoothed'] = df['acc_angle_corrected_alt'].iloc[0]

for i in range(1, len(df)):
    df.loc[i, 'comp_angle_smoothed'] = (alpha * (df['comp_angle_smoothed'].iloc[i-1] + df['gyrZ_smoothed'].iloc[i] * df['delta_time'].iloc[i])) + ((1 - alpha) * df['acc_angle_corrected_alt'].iloc[i])

# Plotting the results
plt.figure(figsize=(14, 14))

# Gyroscope Z-axis
plt.subplot(3, 1, 1)
plt.plot(x_axis, df['gyrZ'], label='Original gyrZ', alpha=0.5)
plt.plot(x_axis, df['gyrZ_smoothed'], label='Smoothed gyrZ', linewidth=2)
plt.title('Gyroscope Z-axis Readings: Original vs Smoothed')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope Z (degrees)')
plt.legend()

# Alternative Corrected Accelerometer angle
plt.subplot(3, 1, 2)
plt.plot(x_axis, df['acc_angle_corrected_alt'], label='Alternative Corrected Accelerometer Angle', linewidth=2)
plt.title('Alternative Corrected Accelerometer Calculated Angle')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Tilt Angle (degrees)')
plt.legend()

# Complementary Filter Angle
plt.subplot(3, 1, 3)
plt.plot(x_axis, df['comp_angle'], label='Complementary Filter Angle', linewidth=2)
plt.plot(x_axis, df['comp_angle_smoothed'], label='Complementary Filter Smoothed Angle', linewidth=2)
plt.title('Calculated Lean Angle using Complementary Filter (Original and Smoothed)')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Lean Angle (degrees)')
plt.legend()

plt.tight_layout()
plt.show()
