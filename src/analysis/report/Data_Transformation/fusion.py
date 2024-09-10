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

# Recalculate delta_time
df['delta_time'] = np.diff(df['seconds'], prepend=df['seconds'].iloc[0])

# Recalculate the tilt angle using atan2(accY, accZ)
df['acc_angle_corrected_alt'] = np.arctan2(df['accY'], df['accZ']) * 180 / np.pi

# Adjust gyroscope data by subtracting the bias
gyro_bias = df['gyrZ'].iloc[:100].mean()
df['gyrZ_bias_corrected'] = df['gyrZ'] - gyro_bias

# Initialize variables for complementary filter with bias-corrected gyroscope data
alpha = 0.95  # Filter coefficient

# Initialize complementary filter with bias-corrected data
df.loc[0, 'comp_angle_bias_corrected'] = df['acc_angle_corrected_alt'].iloc[0]

# Apply complementary filter using bias-corrected gyrZ and the alternative corrected accelerometer angle
for i in range(1, len(df)):
    df.loc[i, 'comp_angle_bias_corrected'] = (
        alpha * (df['comp_angle_bias_corrected'].iloc[i-1] + df['gyrZ_bias_corrected'].iloc[i] * df['delta_time'].iloc[i])
    ) + ((1 - alpha) * df['acc_angle_corrected_alt'].iloc[i])

# Rotate accY and accZ to remove lean effects using comp_angle_bias_corrected
# Convert comp_angle_bias_corrected from degrees to radians
df['comp_angle_bias_corrected_rad'] = np.deg2rad(df['comp_angle_bias_corrected'])

# Apply rotation matrix to accY and accZ
df['accY_earth'] = df['accY'] * np.cos(df['comp_angle_bias_corrected_rad']) - df['accZ'] * np.sin(df['comp_angle_bias_corrected_rad'])
df['accZ_earth'] = df['accY'] * np.sin(df['comp_angle_bias_corrected_rad']) + df['accZ'] * np.cos(df['comp_angle_bias_corrected_rad'])

# Remove gravity from the Z-axis (Earth frame)
g = 9.81  # Gravitational acceleration (m/s²)
df['accZ_earth'] = df['accZ_earth'] - g

# Plot the original and corrected accelerations and the tilt angle

plt.figure(figsize=(12, 12))

# Plot X-axis acceleration (unchanged)
plt.subplot(4, 1, 1)
plt.plot(df['seconds'], df['accX'], label='Original accX', alpha=0.6)
plt.title('Acceleration X-axis (Motorcycle frame)')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration X (mg)')
plt.legend()

# Plot Y-axis acceleration (original vs corrected)
plt.subplot(4, 1, 2)
plt.plot(df['seconds'], df['accY'], label='Original accY', alpha=0.6)
plt.plot(df['seconds'], df['accY_earth'], label='Corrected accY (Earth frame)', color='orange')
plt.title('Acceleration Y-axis (Original vs Corrected for Lean)')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration Y (mg)')
plt.legend()

# Plot Z-axis acceleration (original vs corrected and gravity removed)
plt.subplot(4, 1, 3)
plt.plot(df['seconds'], df['accZ'], label='Original accZ', alpha=0.6)
plt.plot(df['seconds'], df['accZ_earth'], label='Corrected accZ (Earth frame, gravity removed)', color='green')
plt.title('Acceleration Z-axis (Original vs Corrected for Lean and Gravity Removed)')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration Z (mg)')
plt.legend()

# Plot the complementary filter angle
plt.subplot(4, 1, 4)
plt.plot(df['seconds'], df['comp_angle_bias_corrected'], label='Lean Angle (comp_angle_bias_corrected)', color='red')
plt.title('Lean Angle (comp_angle_bias_corrected)')
plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.legend()

plt.tight_layout()
plt.show()
