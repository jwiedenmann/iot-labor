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

# Apply pitch correction for sensor mounting angle (-11.16 degrees)
pitch_angle_rad = np.deg2rad(11.5)  # Convert to radians for the pitch correction
cos_pitch = np.cos(pitch_angle_rad)
sin_pitch = np.sin(pitch_angle_rad)

# Correct the X and Z axes using the pitch correction
df['accX_corrected'] = df['accX'] * cos_pitch + df['accZ'] * sin_pitch
df['accZ_corrected'] = -df['accX'] * sin_pitch + df['accZ'] * cos_pitch

# Rotate accY and accZ using the complementary filter angle (comp_angle_bias_corrected)
df['comp_angle_bias_corrected_rad'] = np.deg2rad(df['comp_angle_bias_corrected'])

df['accY_earth'] = df['accY'] * np.cos(df['comp_angle_bias_corrected_rad']) - df['accZ_corrected'] * np.sin(df['comp_angle_bias_corrected_rad'])

# Convert corrected accelerometer values to g-forces
g_force_conversion = 9.81  # Earth's gravitational constant

df['accX_g_force'] = df['accX_corrected'] / g_force_conversion
df['accY_g_force'] = df['accY_earth'] / g_force_conversion

# Plot peak g-forces with accY_g_force on X-axis and accX_g_force on Y-axis (without Z-axis)
plt.figure(figsize=(10, 8))
plt.scatter(df['accY_g_force'], df['accX_g_force'], alpha=0.6, color='blue', s=10)
plt.title('Peak G-Forces: Corrected accX vs Corrected accY')
plt.xlabel('Corrected Lateral Acceleration (g-force, accY)')
plt.ylabel('Corrected Longitudinal Acceleration (g-force, accX)')
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
