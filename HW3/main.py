import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# read the csv files
airports = pd.read_csv("airports.dat")
no_covid = pd.read_csv("otselennud.csv", sep=';')
covid = pd.read_csv("flights22.csv", sep=';')

# merge no covid flights
output_no_covid = pd.merge(no_covid, airports, on='IATA')

# merge covid flights
output_covid = pd.merge(covid, airports, on='IATA')

# set the latitude and longitude of Tallinn
TLL_lat = 0
TLL_lon = 0
for index, row in output_no_covid.iterrows():
    if row["IATA"] == "TLL":
        TLL_lat = row["Latitude"]
        TLL_lon = row["Longitude"]

# create a map of Europe with Tallinn on it
proj = ccrs.Miller()
ax = plt.axes(projection=proj)
ax.set_extent([-20, 45, 25, 70])
ax.stock_img()
ax.add_feature(cf.COASTLINE, lw=2)
ax.add_feature(cf.BORDERS)
plt.gcf().set_size_inches(20, 10)
plt.text(TLL_lon, TLL_lat, 'Tallinn',
         transform=ccrs.Geodetic(),
         horizontalalignment='right')

# iterate through no covid flights and add the trajectory to the map in blue color
for index, row in output_no_covid.iterrows():
    plt.plot([TLL_lon, row["Longitude"]], [TLL_lat, row["Latitude"]],
             color='blue', transform=ccrs.Geodetic(), marker='o')
    plt.text(row["Longitude"], row["Latitude"], row["City_x"],
             transform=ccrs.Geodetic(),
             fontsize=12)

# iterate through covid flights and add the trajectory to the map in red color
for index, row in output_covid.iterrows():
    plt.plot([TLL_lon, row["Longitude"]], [TLL_lat, row["Latitude"]],
             color='red', transform=ccrs.Geodetic(),  marker='o')
    plt.text(row["Longitude"], row["Latitude"], row["City_x"],
             transform=ccrs.Geodetic(),
             fontsize=12)

# add title and author
plt.title("Flights from Tallinn\nAuthor: Edvin Ess")

# adding custom lines for the legend
custom_lines = [Line2D([0], [0], color='red', lw=4),
                Line2D([0], [0], color='blue', lw=4)]

# adding legend
plt.legend(custom_lines, ['Covid', 'No Covid'], loc="upper right")

# showing and saving it as png file
plt.savefig("EdvinEssMap.png")
plt.show()
