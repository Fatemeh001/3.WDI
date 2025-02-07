import pandas as pd
import numpy as np
import lightningchart as lc
from scipy.interpolate import griddata

# License setup
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'D:/fatemeh_ajam/lightningChart/3.WDi/allcleanData_filled.csv'
data = pd.read_csv(file_path)



# Filter for China and relevant indicators
china_data = data[data['Country Name'] == 'China']
three_d_data = china_data[china_data['Indicator Code'].isin([
    'NY.GDP.MKTP.KD.ZG',  # GDP Growth (annual %)
    'FP.CPI.TOTL.ZG',     # Inflation, consumer prices (annual %)
    'FM.LBL.BMNY.GD.ZS'   # Broad Money Supply (% of GDP)
])]

# Extracting year and values for the indicators
available_years = [col for col in china_data.columns if col.isdigit()]
three_d_long = three_d_data.melt(
    id_vars=['Country Name', 'Indicator Code'],
    value_vars=available_years,
    var_name='Year',
    value_name='Value'
)
three_d_long['Year'] = three_d_long['Year'].astype(int)

# Pivot data for surface plot
three_d_pivot = three_d_long.pivot_table(index='Year', columns='Indicator Code', values='Value').dropna()
x = three_d_pivot['NY.GDP.MKTP.KD.ZG']    # GDP Growth
y = three_d_pivot['FP.CPI.TOTL.ZG']       # Inflation
z = three_d_pivot['FM.LBL.BMNY.GD.ZS']    # Broad Money Supply

# Grid data for 3D surface plot
X, Y = np.meshgrid(np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100))
Z = griddata((x, y), z, (X, Y), method='cubic')  # Use 'cubic' for smoother interpolation
Z[np.isnan(Z)] = np.nanmean(z)  # Handle NaN by filling with average value

# Set up the LightningChart 3D surface chart
chart = lc.Chart3D(
    theme=lc.Themes.Light,
    title='3D Surface of GDP Growth, Inflation, and Broad Money Supply'
)

surface_series = chart.add_surface_grid_series(
    columns=Z.shape[1],
    rows=Z.shape[0]
)

# Set up dimensions and grid parameters
surface_series.set_start(x=x.min(), z=y.min())
surface_series.set_end(x=x.max(), z=y.max())
surface_series.set_step(
    x=(x.max() - x.min()) / Z.shape[1],
    z=(y.max() - y.min()) / Z.shape[0]
)

# Update height map and intensity values
surface_series.invalidate_height_map(Z.tolist())
surface_series.invalidate_intensity_values(Z.tolist())

# Set color shading for smoother surface
surface_series.set_color_shading_style(phong_shading=True, specular_reflection=0.3)

# Customize palette colors with Viridis color scheme and specific value range
surface_series.set_palette_coloring(
    steps=[
        {"value": -200, "color": lc.Color(68, 1, 84)},      
        {"value": -100, "color": lc.Color(59, 82, 139)},    
        {"value": 0, "color": lc.Color(33, 145, 140)},     
        {"value": 100, "color": lc.Color(94, 201, 98)},    
        {"value": 200, "color": lc.Color(253, 231, 37)}     
    ],
    look_up_property='value',
    interpolate=True, 
    percentage_values=False
)

# Customize axis labels and background color to match Matplotlib style
chart.get_default_x_axis().set_title('GDP Growth (annual %)')
chart.get_default_y_axis().set_title('Broad Money Supply (% of GDP)')
chart.get_default_z_axis().set_title('Inflation (Consumer Prices %)')
chart.set_background_color(lc.Color(255, 255, 255))  



# Add legend
chart.add_legend(data=surface_series)

# Display chart
chart.open()



