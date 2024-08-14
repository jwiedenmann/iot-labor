import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = 'C:\\Users\\jwiedenmann\\source\\dhbw_projects\\iot-labor\\data\\test.csv'
df = pd.read_csv(file_path, delimiter=';')

# Define the columns to clean
sensor_columns = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ', 'magX', 'magY', 'magZ', 'temp']

# Replace values above 10000 or below -10000 with NaN
df[sensor_columns] = df[sensor_columns].applymap(lambda x: np.nan if x > 10000 or x < -10000 else x)

# Toggle variable to choose between 'millis' or range(len(millis)) for the x-axis
use_millis = False  # Set this to True to use 'millis', or False to use the index range

x_axis = df['millis'] if use_millis else range(len(df['millis']))

plt.figure(figsize=(14, 10))

# Time Series Plot for Accelerometer, Gyroscope, and Magnetometer readings
plt.subplot(3, 1, 1)
plt.plot(x_axis, df['accX'], label='accX')
plt.plot(x_axis, df['accY'], label='accY')
plt.plot(x_axis, df['accZ'], label='accZ')
plt.title('Cleaned Accelerometer Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Acceleration (accX, accY, accZ)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(x_axis, df['gyrX'], label='gyrX')
plt.plot(x_axis, df['gyrY'], label='gyrY')
plt.plot(x_axis, df['gyrZ'], label='gyrZ')
plt.title('Cleaned Gyroscope Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope (gyrX, gyrY, gyrZ)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(x_axis, df['magX'], label='magX')
plt.plot(x_axis, df['magY'], label='magY')
plt.plot(x_axis, df['magZ'], label='magZ')
plt.title('Cleaned Magnetometer Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Magnetometer (magX, magY, magZ)')
plt.legend()

plt.tight_layout()
plt.show()

# Correlation Matrix for cleaned data
plt.figure(figsize=(10, 8))
corr_matrix = df[sensor_columns].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Cleaned Sensor Readings')
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
plt.show()
