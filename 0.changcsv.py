import pandas as pd

# Load the data
file_path = 'D:/fatemeh_ajam/lightningChart/3.WDi/finalcleanData_filled.csv'
data = pd.read_csv(file_path)

# Reshape the data to have a 'Year' column instead of individual year columns
data_melted = data.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                        var_name='Year', value_name='Value')

# Rename columns to match the required names
data_melted.columns = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Year', 'Value']

# Save the transformed data to a new CSV file
output_file_path = 'transformed_data.csv'
data_melted.to_csv(output_file_path, index=False)

print(f"Transformed data saved to {output_file_path}")
