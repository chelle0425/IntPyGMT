### imports ###
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.image as mpimg 
from mpl_toolkits.basemap import Basemap

import pygmt
from pygmt.clib import Session
from pygmt.helpers import GMTTempFile

%matplotlib widget

### functions ###

def mercator_png(png_path, llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, grid_freq):
    '''
    Creates an interactive map from a borderless pyGMT png where you can click to retrieve coordinates.
    Will work only for mercator projection.

    Parameters:
        png_path (str): path to the borderless pyGMT map
        llcrnrlon (float): lower left corner longitude
        llcrnrlat (float): lower left corner latitude
        urcrnrlon (float): upper right corner longitude
        urcrnrlat (float): upper right corner latitude
        grid_freq (float): grid frequency (degrees) on matplotlib

        
    Example (see demo_borderless_mercator_png):
        llcrnrlon=62
        llcrnrlat=32.65
        urcrnrlon=72.8
        urcrnrlat=38.65 
        grid_freq = 2
        mercator_png("Herat_InSAR_stc.png", llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, grid_freq)
    '''

    # determine image dimension
    img = Image.open(png_path)
    width, height = img.size # (width,height) tuple in pixels
    DPI_horz, DPI_vert = img.info.get('dpi')

    assert DPI_horz == DPI_vert

    fig = plt.figure(figsize=(width/DPI_horz, height/DPI_horz))
    ax1 = plt.subplot(111)

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

def gmt_png(png_path, region, projection, xshift, yshift):
    '''
    Creates an interactive map from a borderless pyGMT png where you can click to retrieve coordinates.

    Parameters:
        png_path (str): path to the borderless PyGMT map
        region (str/ list): pygmt region input
        projection (str): pygmt map projection input
        xshift: xshift left from bottom left corner relative to background canvas
        yshift: yshift upwards from bottom-most basemap extent relative to background canvas

    Example (see demo_conical/cascadia.ipynb):

        region=[-136, -118.5, 38.5, 53.1]
        projection="B-127.25/45.8/43.19/47.86/11c"

        %matplotlib widget
        gmt_png("cascadia.png", region, projection, "2c", "5c")

    '''

    ########## inputs ##########
    # turn pygmt region input into gmt str
    if isinstance(region, str):
      region_str = region
    elif isinstance(region, list):
      region_str = f"{region[0]}/{region[1]}/{region[2]}/{region[3]}"
    else:
      raise Exception("invalid region input (must be either a str or a list)") 


    # unpact xshift yshift
    def unpack_xyshift(str):
      if str[-1].isalpha():
        shift_value = str[:-1]
        shift_unit = str[-1]

      else: 
        raise Exception("invalid xshift or yshift input") 
      
      return float(shift_value), shift_unit


    xshift_value, xshift_unit = unpack_xyshift(xshift)
    yshift_value, yshift_unit = unpack_xyshift(yshift)

    # we are working in cm
    if xshift_unit == "c":
      xshift_value = xshift_value
    elif xshift_unit == "i":
      xshift_value = xshift_value * 2.54
    elif xshift_unit == "p":
      xshift_value = (xshift_value * 72) * 2.54
    else:
      raise Exception("invalid xshift input (must be either c, i or p)") 
      
    # similarly for y
    if yshift_unit == "c":
      yshift_value = yshift_value
    elif yshift_unit == "i":
      yshift_value = yshift_value * 2.54
    elif yshift_unit == "p":
      yshift_value = (yshift_value * 72) * 2.54
    else:
      raise Exception("invalid yshift input (must be either c, i or p)") 
    

    # determine image dimension
    img = Image.open(png_path)
    width, height = img.size # canvas (width,height) tuple in pixels
    DPI_horz, DPI_vert = img.info.get('dpi')

    assert DPI_horz == DPI_vert # is this != even possible??  what about 299.9999994 vs 299.9999995 ?


    ################################################
    ########## plots ##########
    fig = plt.figure(figsize=(width/DPI_horz, height/DPI_vert))
    ax1 = plt.subplot(111)

    '''
    code above doesnt "work' in the sense that its unnecessary
    as figure size != subplot axis size --> what to do with multiple subplots eg timeseries
    edit: subplot axis is currently set to image pixel size so ok now
    '''

    # plotting pygmt png image in bottom layer
    img = mpimg.imread(png_path)

    plt.imshow(img, origin='upper')
    # SOMEHOW MATPLOTLIB MIRRORS MY IMAGE WHEN I SET (0,0) AS BOTTOM LEFT (origin='lower')
    # i fix this later directly at pos_to_lonlat (by reversing input)

    
    def pos_to_lonlat(x, y):
      # xyshift input in cm
      x=(x/DPI_horz) * 2.54 # convert pixel to cm
      x = x - xshift_value

      y=(y/DPI_vert) * 2.54 # cm
      height_cm = (height/DPI_vert) * 2.54
      y = height_cm - y - yshift_value
      
      x=[x] # must be list with one value or np array
      y=[y]
      
      ### lon lat conversion using mapproject ###
      with Session() as ses:
        with ses.virtualfile_from_vectors(x, y) as fin:
          args = [f'{fin}', f'-R{region_str}', f'-J{projection}', '-I']
          with GMTTempFile() as fout:
            ses.call_module(module="mapproject", args=' '.join(args)+ " ->" + fout.name)
            out = fout.read().strip()

      lon, lat = [float(i) for i in out.split(' ')]
    
      return lon, lat


    pos = [] # in format [[None, None], [x, y], [x, y], ...]
    lonlat = []

    def onclick(event):
      pos.append([event.xdata, event.ydata])

      lon, lat = pos_to_lonlat(float(pos[-1][0]), float(pos[-1][1]))
      # converts x y to lon lat and appends
      # pos[-1] represents last click (list with x, y)
      # this is x y input in pixels --> need to convert to cm (gmt input)
      lonlat.append([lon, lat])

      ax1.set_title(f'Click {len(pos)}: {lon}, {lat}')

    
    cid=fig.canvas.mpl_connect('button_press_event', onclick)

    plt.axis('off')
    #plt.show()

    return ax1


# example
# ax1 = gmt_png(png_path, region, projection, xshift, yshift)

def coords_from_figure(ax1):
    coords = ax1.get_title().split()
    lat = float(coords[-1])
    lon = float(coords[-2].split(',')[0])
    return lon, lat


'''
The proper approach should be something like:

class IntPygmtPlot(....):
    def __init__(...):
        ... most of your code above
    
    def pos_to_lonlat(x, y):
        ...
    ...
    def plot(interactive = True, onclickF = onclick):
        ax1 = plt.subplot...
        if interactive:
            fig.canvas.mpl_connect('button_press_event', onclickF)


Because then you can do something like
thisfig =  IntPygmtPlot(png_path=..., )
thisfig.plot(onclickF = tsplot)

'''