# IntPyGMT
A simple code that overlays a matplotlib widget on top of a _borderless_ PyGMT png to enable coordinate selection.

### Installation
This code works in conjunction with PyGMT virtual environment (see https://www.pygmt.org/latest/install.html)

Initialize PyGMT environment
```
conda create --name pygmt --channel conda-forge pygmt
conda activate pygmt
```

Install the library
```
pip install IntPyGMT@git+https://github.com/chelle0425/IntPyGMT.git
```

To use on top of a _borderless_ PyGMT basemap (eg "test.png"):

```
from IntPyGMT.IntPyGMT_overlay import interactive_pygmt
%matplotlib widget

interactive_pygmt("test.png", llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, grid_freq)
```
