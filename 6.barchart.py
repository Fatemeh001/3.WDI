import pandas as pd
import lightningchart as lc

# Load the data
file_path = 'D:/fatemeh_ajam/lightningChart/3.WDi/finalcleanData_filled.csv'
data = pd.read_csv(file_path)

# License setup
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Define the groups for the indicators
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
                       'CM.MKT.TRAD.GD.ZS', 'BN.CAB.XOKA.GD.ZS'],
}

# Create the bar chart
bar_chart = lc.BarChart(theme=lc.Themes.Light, title="Bar Chart of Economic Indicators for China")

# Data for the bar chart
bar_data = []

# Loop through each group and calculate total values
for group, indicators in indicator_groups.items():
    total_value = 0
    for indicator in indicators:
        country_data = data[(data['Country Name'] == 'China') & (data['Indicator Code'] == indicator)]
        if not country_data.empty:
            value = country_data['2022'].values[0]  # Get value for 2022
            total_value += value
        else:
            print(f"No data for {indicator}, using value 0")  # Print message and use value 0
            total_value += 0  # Append 0 if no data

    # If total_value is still NaN, set it to 0
    if pd.isna(total_value):
        total_value = 0

    # Append the group's total value to the bar_data
    bar_data.append({'category': group, 'value': total_value})



# Set data for the bar chart
bar_chart.set_data(bar_data)

# Set additional properties for the bar chart
bar_chart.set_sorting("descending")  # Sort the bars in descending order
bar_chart.set_label_fitting(True)  # Enable automatic label fitting
bar_chart.set_value_label_display_mode('afterBar')  # Display value labels after bars

# Open the bar chart
bar_chart.open()



