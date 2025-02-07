

import pandas as pd
import lightningchart as lc
import time
import numpy as np
import random

# Load the transformed data
data = pd.read_csv('D:/fatemeh_ajam/lightningChart/3.WDi/transformed_data.csv')

# License key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Define indicator groups
indicator_groups = {
    'Agriculture': ['NV.AGR.TOTL.ZS'],
    'Finance': ['FM.LBL.BMNY.GD.ZS', 'FS.AST.PRVT.GD.ZS', 'FD.AST.PRVT.GD.ZS', 'GC.TAX.TOTL.GD.ZS'],
    'Natural Resources': ['NY.GDP.COAL.RT.ZS', 'NY.GDP.MINR.RT.ZS', 'NY.GDP.NGAS.RT.ZS', 'NY.GDP.PETR.RT.ZS'],
    'Trade': ['NE.EXP.GNFS.ZS', 'NE.IMP.GNFS.ZS', 'NE.TRD.GNFS.ZS'],
    'Investment': ['BX.KLT.DINV.WD.GD.ZS', 'BM.KLT.DINV.WD.GD.ZS', 'NE.GDI.TOTL.ZS', 'NE.GDI.FPRV.ZS'],
    'Consumption': ['NE.CON.GOVT.ZS', 'NE.CON.PRVT.ZS', 'NE.CON.TOTL.ZS'],
    'Social Sectors': ['SH.XPD.CHEX.GD.ZS', 'SH.XPD.GHED.GD.ZS'],
    'Military': ['MS.MIL.XPND.GD.ZS'],
    'Overall Economy': ['NY.GDP.FRST.RT.ZS', 'NY.GDP.TOTL.RT.ZS', 'TG.VAL.TOTL.GD.ZS', 'GC.DOD.TOTL.GD.ZS', 
                        'GC.XPN.TOTL.GD.ZS', 'BG.GSR.NFSV.GD.ZS', 'CM.MKT.LCAP.GD.ZS', 'GC.AST.TOTL.GD.ZS', 
                        'GC.LBL.TOTL.GD.ZS', 'GC.NFN.TOTL.GD.ZS', 'GC.NLD.TOTL.GD.ZS', 'GB.XPD.RSDV.GD.ZS', 
                        'CM.MKT.TRAD.GD.ZS', 'BN.CAB.XOKA.GD.ZS']
}

# Filter data for China
country_data = data[data['Country Name'] == 'World']

# Initialize the polar chart
chart = lc.PolarChart(theme=lc.Themes.Light, title="Normalized Indicator Groups for China")

# Generate random color function
def get_random_color():
    return lc.Color(f'#{random.randint(0, 0xFFFFFF):06x}')

# List of years and their angles for the polar chart
years = sorted(country_data['Year'].unique())
angles = np.linspace(0, 360, len(years), endpoint=False)

# Initialize the legend
legend = lc.ui.legend.Legend(chart, horizontal=False, title="Indicator Groups")

# Create line series for each group and add normalized data
for group_name, indicators in indicator_groups.items():
    # Filter data for the indicators in the current group and calculate the mean for each year
    group_data = country_data[country_data['Indicator Code'].isin(indicators)]
    group_data = group_data.groupby('Year')['Value'].mean().reindex(years).fillna(0)
    
    # Normalize the data (Min-Max Normalization)
    normalized_values = (group_data - group_data.min()) / (group_data.max() - group_data.min())
    
    # Prepare data points for the polar chart
    data_points = [{'angle': angle, 'amplitude': value} for angle, value in zip(angles, normalized_values)]
    
    # Add the line series to the chart and to the legend
    line_series = chart.add_point_line_series().set_name(group_name)
    line_series.set_data(data_points)
    line_series.set_stroke(thickness=2, color=get_random_color())
    legend.add(line_series)  # Add series directly to the legend

# Customize radial axis labels and divisions for specific years
radial_axis = chart.get_radial_axis()
radial_axis.set_division(27)
radial_axis.set_tick_labels([
    '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
    '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
    '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
    '2020', '2021','2022'
])

# Open the chart
chart.open()