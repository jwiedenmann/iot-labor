import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'C:\\Users\\jwiedenmann\\source\\dhbw_projects\\iot-labor\\data\\test2.csv'
df = pd.read_csv(file_path, delimiter=';')

# Define the columns to clean
sensor_columns = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ', 'temp']

# Replace values above 10000 or below -10000 with NaN using map
for column in sensor_columns:
    df[column] = df[column].map(lambda x: np.nan if x > 10000 or x < -10000 else x)

# Define the size of the rolling window (you can adjust this)
window_size = 3

# Replace NaN values with the local average using a rolling window
for column in sensor_columns:
    df[column] = df[column].fillna(df[column].rolling(window=window_size, min_periods=1, center=True).mean())

# Adjusting the millis values for resets by iterating over them
millis_adjusted = []
offset = 0

for i in range(len(df['millis'])):
    if i > 0 and df['millis'][i] < df['millis'][i - 1]:
        offset += df['millis'][i - 1]  # Add the last value before the reset to the offset
    millis_adjusted.append(df['millis'][i] + offset)

df['millis_adjusted'] = millis_adjusted

# Convert milliseconds to seconds for easier interpretation
df['seconds'] = df['millis_adjusted'] / 1000

# Toggle variable to choose between 'seconds' or range(len(millis)) for the x-axis
use_seconds = True  # Set this to True to use 'seconds', or False to use the index range

x_axis = df['seconds'] if use_seconds else range(len(df['millis_adjusted']))

# Toggle smoothing on or off
smooth_data = True  # Set this to False to disable smoothing
smoothing_window = 10  # Define the window size for smoothing

if smooth_data:
    for column in sensor_columns:
        df[column] = df[column].rolling(window=smoothing_window, min_periods=1, center=True).mean()

# Correlation Analysis between temperature and other columns
correlation_matrix = df[sensor_columns].corr()

# Display the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Plot the correlation heatmap if needed
plt.matshow(correlation_matrix, cmap='coolwarm')
plt.colorbar()
plt.show()
