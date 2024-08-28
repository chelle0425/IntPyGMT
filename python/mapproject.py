'''
https://forum.generic-mapping-tools.org/t/replicate-grdview-t-with-pygmt/5121

with pygmt.clib.Session() as s:
    with s.virtualfile_in(check_kind="raster", data=grd) as vingrd:
        args = [f'{vingrd}', '-T', '-BNSEW', '-Ba.1f.05', '-C']
        s.call_module('grdview', args=' '.join(args))
'''
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
)
@kwargs_to_strings(R="sequence")
def mapproject(
    self, x=None, y=None, **kwargs):
    r"""
    Reads (lon, lat) positions from tables [or standard input] and computes (x, y) coordinates using the specified map projection and scales.
    Optionally, it can read (x, y) positions and compute (lon, lat) values doing the inverse transformation. 

    Must provide ``x``/``y``.

    THIS IS MODIFIED TO MAKE IT WORK WITH MY CODE SOMEONE PLEASE MAKE THIS WORK PROPERLY
    """
    kwargs = self._preprocess(**kwargs)


    with Session() as lib:
        with lib.virtualfile_in(
            x=x, y=y
        ) as vintbl:
            lib.call_module(module="mapproject", args=build_arg_list(kwargs, infile=vintbl))