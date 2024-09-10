# IntPyGMT
IntPyGMT is an open-source Jupyter Notebook library that generates interactive maps from png images where you can click to retrieve map coordinates. It supports two primary functionalities:

#### 1. From a GMT/PyGMT-generated png

Creates an interactive map from a GMT/PyGMT-generated png image. This feature supports all GMT/PyGMT projection systems provided that the correct xshift and yshift parameters are specified.

This works by overlaying an interactive matplotlib widget on top of a GMT/PyGMT-generated png. User's click coordinates are recorded and adjusted for the map's border width (via xshift and yshift) before processed through GMT's mapproject module which returns map coordinates based on the specified region and projection. Please see `demo_conical` for a demonstration.

#### 2. From a _borderless_ png map (in Mercator projection)

Creates an interactive map from a _borderless_ png image **in Mercator projection**. This is not limited to GMT/PyGMT-generated outputs provided that the coordinates of the lower-left and upper-right corners of the map are known.

This works by aligning a matplotlib map on top of a _borderless_ png image. User's click coordinates on the matplotlib map are then directly registered and returned as map coordinates. Please refer to `demo_borderless_mercator_png` and `demo_borderless_mercator_pygmt` for demonstrations.  For an example of this function adapted and applied to an InSAR time-series plot, see `demo_time_series`.

<br />
<figure>
  <img src="https://github.com/user-attachments/assets/1f0e2838-bf10-43e2-af1a-6842ef9418cf" width="680" alt="EW_Herat_demo_pygmt"/> 
</figure>
<br />
<figure>
  <img src="https://github.com/user-attachments/assets/921d3242-2842-498f-8983-f7011c3a873b" width="680" alt="Time_series_demo"/>
</figure>
<br />

## Getting Started
To launch the demo notebook (use this if you want to run through the demos):

To launch the full repo (use this if you want to experiment with the code):


### Installation
This code works in conjunction with PyGMT virtual environment (see https://www.pygmt.org/latest/install.html).
To get a local copy up and running follow these simple example steps.

Clone the repo
```
git clone https://github.com/chelle0425/IntPyGMT.git
```

Navigate to the project directory
```
cd IntPyGMT
```

Initialize PyGMT environment
```
conda create --name pygmt --channel conda-forge pygmt
conda activate pygmt
```

Install the library
```
pip install IntPyGMT@git+https://github.com/chelle0425/IntPyGMT.git
```

### Usage
> [!IMPORTANT]
> Please ensure that matplotlib widget is enabled before you call the function.
> ```
> %matplotlib widget
> ```


To use on top of a GMT/PyGMT-generated png (see `demo_conical/cascadia.ipynb`):

```
from IntPyGMT.IntPyGMT_overlay import gmt_png
%matplotlib widget

region=[-136, -118.5, 38.5, 53.1]
projection="B-127.25/45.8/43.19/47.86/11c"

gmt_png("cascadia.png", region, projection, "2c", "5c")
```


To use on top of a _borderless_ png map (see `demo_borderless_mercator_png/Herat_InSAR_stc.ipynb`):
```
from IntPyGMT.IntPyGMT_overlay import mercator_png
%matplotlib widget

llcrnrlon=62 # lower left corner longitude 
llcrnrlat=32.65 # lower left corner latitude
urcrnrlon=72.8 # upper right corner longitude
urcrnrlat=38.65 # upper right corner latitude
grid_freq = 2
mercator_png("Herat_InSAR_stc.png", llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, grid_freq)
```

## Examples
### GMT/PyGMT png

### Borderless Mercator png

## To Do
- README images and gifs
- Binder
- Cite sources for demos
- Make m.drawcoastlines() and parallels and meridians plot optional for mercator_png()
- Do this the proper way using OOP

## Meta
This is an open-source project, thus contributions and edits are strongly encouraged. GitHub users may open issues or make pull requests for contributions. Alternatively please email me (rochelle.pun@gmail.com) for any suggestions and/ or enquiries.

This project may be freely distributed and modified provided the source is acknowledged explicitly. Please cite the latest release when you do so.

### Acknowledgements
This project was initiated as part of my 3rd-year Independent Project in the Department of Earth Science and Engineering at Imperial College London (see: [MomentTensorSum](https://github.com/chelle0425/MomentTensorSum)). It has greatly benefitted from subsequent development during my time as a COMET research intern at the University of Leeds.

I would like to express my sincerest gratitude to Dr Milan Lazecky, for it was his invaluable guidance and unwavering support that made this project a reality. 

Additionally, I am grateful to COMET, the UK’s Centre for the Observation and Modelling of Earthquakes, Volcanoes and Tectonics, for funding my research internship. It was during this time that we developed the core functionality of the code.

*Version 1.0.0*

<rochelle.pun@gmail.com>, 2024
