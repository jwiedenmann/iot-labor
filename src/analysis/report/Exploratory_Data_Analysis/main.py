import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Toggle variable to choose between 'millis_adjusted' or range(len(millis)) for the x-axis
use_millis = True  # Set this to True to use 'millis_adjusted', or False to use the index range

x_axis = df['millis_adjusted'] if use_millis else range(len(df['millis_adjusted']))

# Toggle smoothing on or off
smooth_data = True  # Set this to False to disable smoothing
smoothing_window = 10  # Define the window size for smoothing

if smooth_data:
    for column in sensor_columns:
        df[column] = df[column].rolling(window=smoothing_window, min_periods=1, center=True).mean()

# Plot and save each sensor's data to separate image files
# Accelerometer Plot
plt.figure(figsize=(14, 10))
plt.plot(x_axis, df['accX'], label='accX')
plt.plot(x_axis, df['accY'], label='accY')
plt.plot(x_axis, df['accZ'], label='accZ')
plt.title('Cleaned Accelerometer Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Acceleration (accX, accY, accZ)')
plt.legend()
plt.savefig('accelerometer_plot.png')
plt.show()

# Gyroscope Plot
plt.figure(figsize=(14, 10))
plt.plot(x_axis, df['gyrX'], label='gyrX')
plt.plot(x_axis, df['gyrY'], label='gyrY')
plt.plot(x_axis, df['gyrZ'], label='gyrZ')
plt.title('Cleaned Gyroscope Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Gyroscope (gyrX, gyrY, gyrZ)')
plt.legend()
plt.savefig('gyroscope_plot.png')
plt.show()

# Magnetometer Plot
plt.figure(figsize=(14, 10))
plt.plot(x_axis, df['magX'], label='magX')
plt.plot(x_axis, df['magY'], label='magY')
plt.plot(x_axis, df['magZ'], label='magZ')
plt.title('Cleaned Magnetometer Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Magnetometer (magX, magY, magZ)')
plt.legend()
plt.savefig('magnetometer_plot.png')
plt.show()

# Temperature Plot
plt.figure(figsize=(14, 10))
plt.plot(x_axis, df['temp'], label='Temperature')
plt.title('Temperature Readings Over Time')
plt.xlabel('Milliseconds' if use_millis else 'Sample Index')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.savefig('temperature_plot.png')
plt.show()

# Generate statistical summary
summary = df[sensor_columns].describe()
print(summary)

# Visualization of the statistical summary (mean, std, min, max)
summary_stats = summary.loc[['mean', 'std', 'min', 'max']].transpose()

# Use a darker theme for better aesthetics
sns.set_theme(style="whitegrid")

# Create a more visually appealing bar plot for the statistical summary
plt.figure(figsize=(16, 10))
sns.barplot(data=summary_stats.reset_index().melt(id_vars='index'), x='index', y='value', hue='variable', palette='Set2')
plt.title('Statistical Summary of Sensor Data', fontsize=20, fontweight='bold')
plt.xlabel('Sensor Type', fontsize=14)
plt.ylabel('Value', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Statistics', title_fontsize='13', loc='upper right')
plt.tight_layout()
plt.savefig('beautiful_statistical_summary_plot.png')
plt.show()

# Generate and save the correlation heatmap
correlation_matrix = df[sensor_columns].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, square=True, linewidths=.5)
plt.title('Correlation Heatmap of Sensor Data', fontsize=18, fontweight='bold')
plt.savefig('correlation_heatmap.png')
plt.show()

# Count the number of non-zero values for each sensor column
non_zero_counts = df[sensor_columns].astype(bool).sum(axis=0)

# Plot the number of non-zero values for each sensor
plt.figure(figsize=(14, 8))
sns.barplot(x=non_zero_counts.index, y=non_zero_counts.values, hue=non_zero_counts.index, dodge=False, palette='Set2', legend=False)
plt.title('Number of Non-Zero Values for Each Sensor', fontsize=20, fontweight='bold')
plt.xlabel('Sensor Type', fontsize=14)
plt.ylabel('Number of Non-Zero Values', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('non_zero_values_plot.png')
plt.show()

# Plot the distribution of accelerometer data in one plot
plt.figure(figsize=(14, 8))
sns.kdeplot(df['accX'], label='accX', shade=True)
sns.kdeplot(df['accY'], label='accY', shade=True)
sns.kdeplot(df['accZ'], label='accZ', shade=True)
plt.title('Distribution of Accelerometer Data', fontsize=20, fontweight='bold')
plt.xlabel('Value', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('accelerometer_distribution_plot.png')
plt.show()

# Plot the distribution of gyroscope data in one plot
plt.figure(figsize=(14, 8))
sns.kdeplot(df['gyrX'], label='gyrX', shade=True)
sns.kdeplot(df['gyrY'], label='gyrY', shade=True)
sns.kdeplot(df['gyrZ'], label='gyrZ', shade=True)
plt.title('Distribution of Gyroscope Data', fontsize=20, fontweight='bold')
plt.xlabel('Value', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('gyroscope_distribution_plot.png')
plt.show()

# Plot the distribution of magnetometer data in one plot
plt.figure(figsize=(14, 8))
sns.kdeplot(df['magX'], label='magX', shade=True)
sns.kdeplot(df['magY'], label='magY', shade=True)
sns.kdeplot(df['magZ'], label='magZ', shade=True)
plt.title('Distribution of Magnetometer Data', fontsize=20, fontweight='bold')
plt.xlabel('Value', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('magnetometer_distribution_plot.png')
plt.show()

# Plot the distribution of temperature data in a separate plot
plt.figure(figsize=(14, 8))
sns.kdeplot(df['temp'], label='Temperature', shade=True)
plt.title('Distribution of Temperature Data', fontsize=20, fontweight='bold')
plt.xlabel('Value', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('temperature_distribution_plot.png')
plt.show()