

import pandas as pd
import lightningchart as lc


file_path = 'D:/fatemeh_ajam/lightningChart/3.WDi/transformed_data.csv'
transformed_data = pd.read_csv(file_path)


with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)


cumulative_indicators_codes = [
    'FM.LBL.BMNY.GD.ZS',  # Broad money supply
    'FS.AST.PRVT.GD.ZS',  # Private sector assets
    'FD.AST.PRVT.GD.ZS',  # Private sector capital assets
    'CM.MKT.TRAD.GD.ZS'   # Market trade value
]


china_cumulative_data = transformed_data[
    (transformed_data['Country Name'] == 'China') &
    (transformed_data['Indicator Code'].isin(cumulative_indicators_codes))
][['Indicator Name', 'Year', 'Value']]


china_cumulative_pivot = china_cumulative_data.pivot(index='Year', columns='Indicator Name', values='Value')


chart = lc.ChartXY(
    title="Cumulative Indicators for China as Percentage of GDP Over Time",
    theme=lc.Themes.Light
)


chart.get_default_x_axis().set_title("Year")
chart.get_default_y_axis().set_title("Percentage of GDP (%)")

for column in china_cumulative_pivot.columns:
    series = chart.add_line_series()
    series.set_name(column)
    series.set_line_thickness(3)  
    series.add(
        x=china_cumulative_pivot.index.tolist(),
        y=china_cumulative_pivot[column].fillna(0).tolist()
    )
    series.set_highlight(True).set_cursor_enabled(True)

chart.add_legend(data=chart).set_position(x=35, y=80)

chart.open()

