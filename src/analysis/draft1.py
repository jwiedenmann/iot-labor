import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = 'C:\\Users\\jwiedenmann\\source\\dhbw_projects\\iot-labor\\data\\2024-08-03.csv'
df = pd.read_csv(file_path, delimiter=';')

# Define the columns to clean
sensor_columns = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ', 'temp']

# Replace values above 10000 or below -10000 with NaN
df[sensor_columns] = df[sensor_columns].map(lambda x: np.nan if x > 10000 or x < -10000 else x)

# Option to save plots
save_plots = True  # Set to True to save the plots to files

# Time Series Plot for Accelerometer, Gyroscope, and Magnetometer readings
plt.figure(figsize=(14, 10))

x_axis = df['insert_time']

plt.subplot(3, 1, 1)
plt.plot(x_axis, df['accX'], label='accX')
plt.plot(x_axis, df['accY'], label='accY')
plt.plot(x_axis, df['accZ'], label='accZ')
plt.title('Cleaned Accelerometer Readings Over Time')
plt.xlabel('Time')
plt.ylabel('Acceleration (accX, accY, accZ)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(x_axis, df['gyrX'], label='gyrX')
plt.plot(x_axis, df['gyrY'], label='gyrY')
plt.plot(x_axis, df['gyrZ'], label='gyrZ')
plt.title('Cleaned Gyroscope Readings Over Time')
plt.xlabel('Time')
plt.ylabel('Gyroscope (gyrX, gyrY, gyrZ)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(x_axis, df['magX'], label='magX')
plt.plot(x_axis, df['magY'], label='magY')
plt.plot(x_axis, df['magZ'], label='magZ')
plt.title('Cleaned Magnetometer Readings Over Time')
plt.xlabel('Time')
plt.ylabel('Magnetometer (magX, magY, magZ)')
plt.legend()

plt.tight_layout()
if save_plots:
    plt.savefig('sensor_time_series.png')
plt.show()

# Correlation Matrix for cleaned data
plt.figure(figsize=(10, 8))
corr_matrix = df[sensor_columns].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Cleaned Sensor Readings')
if save_plots:
    plt.savefig('correlation_matrix.png')
plt.show()

# Distribution Plots for each cleaned sensor's readings
plt.figure(figsize=(14, 12))
for i, col in enumerate(sensor_columns):
    plt.subplot(5, 2, i+1)
    plt.hist(df[col].dropna(), bins=50, color='skyblue', edgecolor='black')
    plt.title(f'Distribution of Cleaned {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')

plt.tight_layout()
if save_plots:
    plt.savefig('sensor_distributions.png')
plt.show()
