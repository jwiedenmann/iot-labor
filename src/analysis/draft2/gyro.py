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
        offset += df['millis'].iloc[i - 1]  # Add the last value before the reset to the offset
    millis_adjusted.append(df['millis'].iloc[i] + offset)

df['millis_adjusted'] = millis_adjusted

# Recalculate time_seconds and delta_time
df['time_seconds'] = df['millis_adjusted'] / 1000
df['delta_time'] = np.diff(df['time_seconds'], prepend=df['time_seconds'].iloc[0])

# Apply Moving Average to reduce noise (window size can be adjusted)
window_size = 20
df['gyrZ_smoothed'] = df['gyrZ'].rolling(window=window_size, center=True).mean()

# Recalculate the tilt angle using atan2(accY, accZ)
df['acc_angle_corrected_alt'] = np.arctan2(df['accY'], df['accZ']) * 180 / np.pi

# Estimate gyroscope bias (assuming the beginning of the data when the motorcycle is stationary)
gyro_bias = df['gyrZ'].iloc[:100].mean()

# Adjust gyroscope data by subtracting the bias
df['gyrZ_bias_corrected'] = df['gyrZ'] - gyro_bias
df['gyrZ_smoothed_bias_corrected'] = df['gyrZ_smoothed'] - gyro_bias

# Initialize variables for complementary filter with bias-corrected gyroscope data
alpha = 0.95  # Adjusted filter coefficient to reduce reliance on gyroscope data

# Reinitialize complementary filter with bias-corrected data
df.loc[0, 'comp_angle_bias_corrected'] = df['acc_angle_corrected_alt'].iloc[0]

# Apply complementary filter using bias-corrected gyrZ and the alternative corrected accelerometer angle
for i in range(1, len(df)):
    df.loc[i, 'comp_angle_bias_corrected'] = (
        alpha * (df['comp_angle_bias_corrected'].iloc[i-1] + df['gyrZ_bias_corrected'].iloc[i] * df['delta_time'].iloc[i])
    ) + ((1 - alpha) * df['acc_angle_corrected_alt'].iloc[i])

# Apply complementary filter for smoothed bias-corrected data
df.loc[0, 'comp_angle_smoothed_bias_corrected'] = df['acc_angle_corrected_alt'].iloc[0]

for i in range(1, len(df)):
    df.loc[i, 'comp_angle_smoothed_bias_corrected'] = (
        alpha * (df['comp_angle_smoothed_bias_corrected'].iloc[i-1] + df['gyrZ_smoothed_bias_corrected'].iloc[i] * df['delta_time'].iloc[i])
    ) + ((1 - alpha) * df['acc_angle_corrected_alt'].iloc[i])

# Plotting the results with the full range of x-axis
plt.figure(figsize=(14, 14))

# Gyroscope Z-axis (Bias Corrected)
plt.subplot(3, 1, 1)
plt.plot(df['millis_adjusted'], df['gyrZ_bias_corrected'], label='Bias Corrected gyrZ', alpha=0.5)
plt.plot(df['millis_adjusted'], df['gyrZ_smoothed_bias_corrected'], label='Bias Corrected Smoothed gyrZ', linewidth=2)
plt.title('Gyroscope Z-axis Readings: Bias Corrected Original vs Smoothed')
plt.xlabel('Milliseconds')
plt.ylabel('Gyroscope Z (degrees)')
plt.legend()

# Alternative Corrected Accelerometer angle
plt.subplot(3, 1, 2)
plt.plot(df['millis_adjusted'], df['acc_angle_corrected_alt'], label='Alternative Corrected Accelerometer Angle', linewidth=2)
plt.title('Alternative Corrected Accelerometer Calculated Angle')
plt.xlabel('Milliseconds')
plt.ylabel('Tilt Angle (degrees)')
plt.legend()

# Complementary Filter Angle with Bias Correction
plt.subplot(3, 1, 3)
plt.plot(df['millis_adjusted'], df['comp_angle_bias_corrected'], label='Complementary Filter Angle (Bias Corrected)', linewidth=2)
plt.plot(df['millis_adjusted'], df['comp_angle_smoothed_bias_corrected'], label='Complementary Filter Smoothed Angle (Bias Corrected)', linewidth=2)
plt.title('Calculated Lean Angle using Complementary Filter (Bias Corrected)')
plt.xlabel('Milliseconds')
plt.ylabel('Lean Angle (degrees)')
plt.legend()

plt.tight_layout()
plt.show()
