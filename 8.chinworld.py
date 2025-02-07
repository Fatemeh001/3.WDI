import pandas as pd
import lightningchart as lc
import numpy as np

# Set your license key here
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load data
data = pd.read_csv('D:/fatemeh_ajam/lightningChart/3.WDi/transformed_data.csv')



# Define all indicator groups and their indicators
indicator_groups = {
    'Agriculture': ['NV.AGR.TOTL.ZS'],
    'Finance': ['FM.LBL.BMNY.GD.ZS', 'FS.AST.PRVT.GD.ZS', 'FD.AST.PRVT.GD.ZS', 'GC.TAX.TOTL.GD.ZS'],
    'Natural Resources': ['NY.GDP.COAL.RT.ZS', 'NY.GDP.MINR.RT.ZS', 'NY.GDP.NGAS.RT.ZS', 'NY.GDP.PETR.RT.ZS'],
    'Trade': ['NE.EXP.GNFS.ZS', 'NE.IMP.GNFS.ZS', 'NE.TRD.GNFS.ZS'],
    'Investment': ['BX.KLT.DINV.WD.GD.ZS', 'BM.KLT.DINV.WD.GD.ZS', 'NE.GDI.TOTL.ZS', 'NE.GDI.FPRV.ZS'],
    'Consumption': ['NE.CON.GOVT.ZS', 'NE.CON.PRVT.ZS', 'NE.CON.TOTL.ZS'],
    'Military': ['MS.MIL.XPND.GD.ZS'],
    'Overall Economy': [
        'NY.GDP.FRST.RT.ZS', 'NY.GDP.TOTL.RT.ZS', 'TG.VAL.TOTL.GD.ZS', 'GC.DOD.TOTL.GD.ZS',
        'GC.XPN.TOTL.GD.ZS', 'BG.GSR.NFSV.GD.ZS', 'CM.MKT.LCAP.GD.ZS', 'GC.AST.TOTL.GD.ZS',
        'GC.LBL.TOTL.GD.ZS', 'GC.NFN.TOTL.GD.ZS', 'GC.NLD.TOTL.GD.ZS', 'GB.XPD.RSDV.GD.ZS',
        'CM.MKT.TRAD.GD.ZS', 'BN.CAB.XOKA.GD.ZS'
    ]
}

# Filter data for China and World
china_data = data[data['Country Name'] == 'China']
world_data = data[data['Country Name'] == 'World']

# List of unique years for consistent angle mapping
years = sorted(china_data['Year'].unique())
angles = np.linspace(0, 360, len(years), endpoint=False)

# Generate and plot each group's PolarChart based on the average of indicators
for group_name, indicators in indicator_groups.items():
    # Calculate average values for each year for China
    china_group_data = china_data[china_data['Indicator Code'].isin(indicators)]
    china_yearly_avg = china_group_data.groupby('Year')['Value'].mean().reindex(years).fillna(0)
    china_normalized = (china_yearly_avg - china_yearly_avg.min()) / (china_yearly_avg.max() - china_yearly_avg.min())
    china_data_points = [{"angle": angle, "amplitude": value} for angle, value in zip(angles, china_normalized)]

    # Calculate average values for each year for World
    world_group_data = world_data[world_data['Indicator Code'].isin(indicators)]
    world_yearly_avg = world_group_data.groupby('Year')['Value'].mean().reindex(years).fillna(0)
    world_normalized = (world_yearly_avg - world_yearly_avg.min()) / (world_yearly_avg.max() - world_yearly_avg.min())
    world_data_points = [{"angle": angle, "amplitude": value} for angle, value in zip(angles, world_normalized)]

    # Create a PolarChart for the current group
    chart = lc.PolarChart(
        title=f"{group_name}: Average of Indicators - China vs World",
        theme=lc.Themes.Light,
    )

    # Add data series for China and World to the chart
    china_series = chart.add_area_series().set_name("China").set_data(china_data_points)
    world_series = chart.add_area_series().set_name("World").set_data(world_data_points)

    # Add the legend
    legend = chart.add_legend(horizontal=False, title=group_name).set_position(x=27.5,y=50)
    legend.add(china_series)  # Add China series to legend
    legend.add(world_series)  # Add World series to legend

    # Open each chart in a separate view
    chart.open()




