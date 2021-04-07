#!/usr/bin/env python3.7.6
# -*- Coding: UTF-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader

# Variable names
main_var = 'alt'

# Filenames
file_in = 'info_est.csv'
feat_file = 'shp/BRA_adm1'
file_out = 'map_%s.png' %main_var

# Load CSV file into DataFrame
df = pd.read_csv(file_in)

# Prepare map
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='',\
 dateline_direction_label=True)
lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# Add feature - political contours
shape_feature = ShapelyFeature(shpreader.Reader(feat_file).geometries(),\
 ccrs.PlateCarree(), facecolor='none', edgecolor='k', linewidth=0.5)
ax.add_feature(shape_feature)

# Plot stations names
for index, row in df.iterrows():
    plt.text(row['lon'],row['lat'],row['id'])

# Add info from DataFrame
normalize = colors.Normalize(vmin=min(df[main_var]), vmax=max(df[main_var]))
cs = ax.scatter(df['lon'].values, df['lat'].values,\
 c=df[main_var].values, cmap=plt.get_cmap('jet'),\
 transform=ccrs.PlateCarree(), marker='o', s=40)

# Add a colorbar
cax, _ = colorbar.make_axes(ax)
cbar = colorbar.ColorbarBase(cax, cmap=plt.get_cmap('jet'),\
 norm=normalize)
cbar.set_label(main_var)

# Plot - show or and save
if file_out == '':
    plt.show()
else:
    plt.savefig(file_out,bbox_inches='tight')
