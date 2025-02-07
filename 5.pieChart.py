import pandas as pd
import lightningchart as lc



# Load the data
file_path = 'D:/fatemeh_ajam/lightningChart/3.WDi/finalcleanData_filled.csv'
data = pd.read_csv(file_path)

# License setup
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Filter data for China in the year 2022
china_data_2022 = data[(data['Country Name'] == 'China') & (data['2022'].notna())][['Indicator Code', '2022']]

# Sort the data by percentage values in descending order
china_data_2022_sorted = china_data_2022.sort_values(by='2022', ascending=False)

# Prepare data in the format required for LightningChart
data_for_chart = [{'name': row['Indicator Code'], 'value': row['2022']} for _, row in china_data_2022_sorted.iterrows()]

# Create the pie chart
chart = lc.PieChart(
    title="China's Indicators in 2022 (as % of GDP)",
    theme=lc.Themes.White
)

# Separate the slices with white stroke
chart.set_slice_stroke(color=lc.Color('white'), thickness=1)

# Add slices to the chart
chart.add_slices(data_for_chart)

# Add legend
chart.add_legend(data=chart)

# Open the chart
chart.open()


