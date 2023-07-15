import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
data = pd.read_csv('Vancouver_data - Vancouver_Full Data_data.csv')

print(data.head)

# Check the number of unique months for each year
unique_months_per_year = data.groupby('Date Of Loss Year')['Month Of Year'].nunique()

# Years that have data for all 12 months
complete_years = unique_months_per_year[unique_months_per_year == 12].index

# Exclude data from incomplete years
data_complete_years = data[data['Date Of Loss Year'].isin(complete_years)]

# Display the years included in the final dataset
print(complete_years)

# 1. Total Number of crashes by day and time

# Group the data by 'Day Of Week' and 'Time Category' and sum the 'Total Crashes'
crashes_by_day_time = data_complete_years.groupby(['Day Of Week', 'Time Category'])['Total Crashes'].sum().reset_index()

# Create an ordered categorical variable to ensure the days are displayed in the correct order on the plot
day_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

# Define the order for the time categories
time_order = ['00:00-02:59', '03:00-05:59', '06:00-08:59', '09:00-11:59', '12:00-14:59', '15:00-17:59', '18:00-20:59',
              '21:00-23:59']

# Create an ordered categorical variable to ensure the time categories are displayed in the correct order on the plot
crashes_by_day_time['Time Category'] = pd.Categorical(crashes_by_day_time['Time Category'], categories=time_order,
                                                      ordered=True)

# Create the plot
plt.figure(figsize=(15, 7))
sns.barplot(x='Day Of Week', y='Total Crashes', hue='Time Category', data=crashes_by_day_time)
plt.title('Total Number of Crashes by Day and Time')
plt.xlabel('Day of Week')
plt.ylabel('Total Crashes')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# 2. Average total crashes by month

# Create an ordered categorical variable to ensure the months are displayed in the correct order on the plot
month_order = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
               'NOVEMBER', 'DECEMBER']

# Group the data by year and month and sum the 'Total Crashes'
total_crashes_per_month_year = data_complete_years.groupby(['Date Of Loss Year', 'Month Of Year'])['Total Crashes'].sum().reset_index()

# Calculate the average total crashes for each month over the years
average_crashes_per_month = total_crashes_per_month_year.groupby('Month Of Year')['Total Crashes'].mean().reset_index()

# Create a new column with chronological month numbers
month_dict = {month: i+1 for i, month in enumerate(month_order)}
average_crashes_per_month['Month Number'] = average_crashes_per_month['Month Of Year'].map(month_dict)

# Sort the DataFrame by the month number
average_crashes_per_month.sort_values('Month Number', inplace=True)

# Recreate the line chart for average total crashes by month with adjusted number positions
# and chronological month order
plt.figure(figsize=(15, 7))
sns.lineplot(x='Month Number', y='Total Crashes', data=average_crashes_per_month, marker='o')

# Show the number of crashes each month on the chart with alignment slightly to the left of data points
for i, row in average_crashes_per_month.iterrows():
    plt.text(row['Month Number'] - 0.2, row['Total Crashes'], round(row['Total Crashes']), color='black',
             ha='center', va='bottom')

plt.title('Average Total Crashes by Month')
plt.xlabel('Month')
plt.ylabel('Average Total Crashes')

# Set the x-tick labels to the month names
plt.xticks(ticks=range(1, 13), labels=month_order, rotation=45)

plt.grid(True)
plt.show()

# 3. Distribution of Crash Severity

# Calculate the count of each crash severity type
crash_severity_counts = data_complete_years['Crash Severity'].value_counts()

# Create the pie chart
plt.figure(figsize=(10, 7))
plt.pie(crash_severity_counts, labels=crash_severity_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Crash Severity')
plt.show()

# 4. Percentage of Casualties in Crashes Involving Cyclists and Pedestrians

# Filter data for crashes involving cyclists and pedestrians with correct case sensitivity
cyclist_crashes = data_complete_years[data_complete_years['Cyclist Flag'] == 'Yes']
pedestrian_crashes = data_complete_years[data_complete_years['Pedestrian Flag'] == 'Yes']

# Get the counts of crash severities for cyclist and pedestrian crashes
cyclist_severity_counts = cyclist_crashes['Crash Severity'].value_counts()
pedestrian_severity_counts = pedestrian_crashes['Crash Severity'].value_counts()

# Convert the counts to percentages
cyclist_severity_percentages = cyclist_severity_counts / cyclist_severity_counts.sum() * 100
pedestrian_severity_percentages = pedestrian_severity_counts / pedestrian_severity_counts.sum() * 100

# Prepare the data for plotting
plot_data = pd.DataFrame({
    'Cyclist Crashes': cyclist_severity_percentages,
    'Pedestrian Crashes': pedestrian_severity_percentages
}).transpose()

# Create the stacked bar chart with adjusted legend and percentage numbers inside bars
ax = plot_data.plot(kind='bar', stacked=True, figsize=(10, 7))

# Move the legend outside the plot area
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# Display percentage numbers inside bars
for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()
    ax.annotate(f'{height:.1f}', (x + width/2, y + height/2), ha='center')

plt.title('Percentage of Casualties in Crashes Involving Cyclists and Pedestrians')
plt.ylabel('Percentage')
plt.xlabel('Crash Type')
plt.show()
