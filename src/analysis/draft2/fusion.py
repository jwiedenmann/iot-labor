import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the updated CSV file
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
        offset += df['millis'].iloc[i - 1]  # Add the last value before the reset to the offset
    millis_adjusted.append(df['millis'].iloc[i] + offset)

df['millis_adjusted'] = millis_adjusted

# Recalculate time_seconds and delta_time
df['time_seconds'] = df['millis_adjusted'] / 1000
df['delta_time'] = np.diff(df['time_seconds'], prepend=df['time_seconds'].iloc[0])

# Apply Moving Average to reduce noise (window size can be adjusted)
window_size = 20
df['gyrZ_smoothed'] = df['gyrZ'].rolling(window=window_size, center=True).mean()

# Calculate the tilt angle using the gyroscope Z-axis data (gyrZ)
# Integrate the gyroscope Z-axis data to obtain the tilt angle over time
df['tilt_angle'] = np.cumsum(df['gyrZ_smoothed'] * df['delta_time'])

# Convert the tilt angle to radians for use in trigonometric functions
df['tilt_angle_rad'] = np.radians(df['tilt_angle'])

# Apply initial bias correction to the acceleration data
# Assuming stationary position at the beginning of the data
accX_bias = df['accX'].iloc[:100].mean()
accY_bias = df['accY'].iloc[:100].mean()
accZ_bias = df['accZ'].iloc[:100].mean() - 9.81  # Subtracting gravity

df['accX_corrected'] = df['accX'] - accX_bias
df['accY_corrected'] = df['accY'] - accY_bias
df['accZ_corrected'] = df['accZ'] - accZ_bias

# Load the lean angle from the complementary filter (assuming it has been calculated in gyro.py)
# For demonstration, I'll use the calculated tilt angle as a placeholder
df['lean_angle_rad'] = np.radians(df['tilt_angle'])  # Replace with actual lean angle from complementary filter

# Apply rotation based on the lean angle to correct the acceleration data
df['accX_corrected_lean'] = df['accX_corrected'] * np.cos(df['lean_angle_rad']) - df['accZ_corrected'] * np.sin(df['lean_angle_rad'])
df['accY_corrected_lean'] = df['accY_corrected']  # Y remains unchanged as the lean is in the X-Z plane
df['accZ_corrected_lean'] = df['accX_corrected'] * np.sin(df['lean_angle_rad']) + df['accZ_corrected'] * np.cos(df['lean_angle_rad'])

# Plot the corrected acceleration data using the lean angle from the complementary filter
plt.figure(figsize=(14, 10))

# Corrected Acceleration X-axis with Lean Angle Correction
plt.subplot(3, 1, 1)
plt.plot(df['millis_adjusted'], df['accX_corrected_lean'], label='Corrected accX with Lean Angle Correction', linewidth=2)
plt.title('Corrected Acceleration X-axis Readings (Lean Angle Correction)')
plt.xlabel('Milliseconds')
plt.ylabel('Acceleration X (m/s²)')
plt.legend()

# Corrected Acceleration Y-axis (unchanged)
plt.subplot(3, 1, 2)
plt.plot(df['millis_adjusted'], df['accY_corrected_lean'], label='Corrected accY', linewidth=2)
plt.title('Corrected Acceleration Y-axis Readings')
plt.xlabel('Milliseconds')
plt.ylabel('Acceleration Y (m/s²)')
plt.legend()

# Corrected Acceleration Z-axis with Lean Angle Correction
plt.subplot(3, 1, 3)
plt.plot(df['millis_adjusted'], df['accZ_corrected_lean'], label='Corrected accZ with Lean Angle Correction', linewidth=2)
plt.title('Corrected Acceleration Z-axis Readings (Lean Angle Correction)')
plt.xlabel('Milliseconds')
plt.ylabel('Acceleration Z (m/s²)')
plt.legend()

plt.tight_layout()
plt.show()
