### imports ###
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.image as mpimg 
from mpl_toolkits.basemap import Basemap


### interactive pygmt the function ##

def interactive_pygmt(png_path, llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, grid_freq):
    '''
    Creates an interactive map from a borderless pyGMT png where you can click to retrieve coordinates.

    Parameters:
        png_path (str): path to the borderless pyGMT map
        llcrnrlon (float): lower left corner longitude
        llcrnrlat (float): lower left corner latitude
        urcrnrlon (float): upper right corner longitude
        urcrnrlat (float): upper right corner latitude
        grid_freq (float): grid frequency (degrees)

    '''

    # determine image dimension
    img = Image.open(png_path)
    width, height = img.size # (width,height) tuple in pixels
    DPI_horz, DPI_vert = img.info.get('dpi')

    assert DPI_horz == DPI_vert

    fig = plt.figure(figsize=(width/DPI_horz, height/DPI_horz))
    ax1 = fig.add_axes([1, 1, 1, 1])

    # creating matplotlib basemap for overlay
    m = Basemap(projection='merc', resolution='i',\
                            llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,\
                            llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon)
    
    m.drawcoastlines() # draws coastlines on matplotlib. this makes sure that everything is aligned

    # plotting parallels and meridians, annotating axis
    parallels = np.arange(-90, 90, grid_freq)
    meridians = np.arange(-180, 180, grid_freq)
    m.drawparallels(parallels, labels=[1,0,0,0], fontsize=12, linewidth=0.5) # label parallels on right and top
    m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=12, linewidth=0.5) # meridians on bottom and left

    # plotting pygmt png image in bottom layer
    img = mpimg.imread(png_path)
    m.imshow(img, origin='upper')


    def pos_to_lonlat(x, y):
      lon, lat = m(x, y, inverse=True)
      return lon, lat
    
    pos = [] # in format [[None, None], [x, y], [x, y], ...]
    lonlat = []

    def onclick(event):
      pos.append([event.xdata, event.ydata])

      lon, lat = pos_to_lonlat(pos[-1][0], pos[-1][1]) # pos[-1] represents last click (list with x, y)
      lonlat.append([lon, lat]) # converts x y to lon lat and appends

      ax1.set_title(f'Click {len(pos)}: {lon}, {lat}') 

    
    cid=fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return