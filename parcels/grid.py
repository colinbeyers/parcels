import numpy as np

from parcels.numba.grid.curvilinear import CurvilinearSGrid, CurvilinearZGrid
from parcels.numba.grid.rectilinear import RectilinearSGrid, RectilinearZGrid
from parcels.tools.converters import TimeConverter


class Grid():
    """Python Grid that is a wrapper around the Numba Grid class."""
    def __init__(self, lon=None, lat=None, depth=None, time=None, mesh=None,
                 time_origin=None, grid=None, **kwargs):
        time_origin = TimeConverter(0) if time_origin is None else time_origin

        if grid is not None and not isinstance(grid, Grid):
            self.numba_grid = grid
            self.time_origin = time_origin
            return
        self.time_origin = time_origin
        self.numba_grid = None
        if not isinstance(lon, np.ndarray):
            lon = np.array(lon)
        if not isinstance(lat, np.ndarray):
            lat = np.array(lat)
        if not isinstance(time, np.ndarray):
            time = np.array(time)
        time = time.astype(np.float64)
        if not (depth is None or isinstance(depth, np.ndarray)):
            depth = np.array(depth)
        if depth is not None:
            depth = depth.astype(np.float32)
        if len(lon.shape) <= 1:
            if depth is None or len(depth.shape) <= 1:
                self.numba_grid = RectilinearZGrid(
                    lon, lat, depth, time, mesh=mesh,
                    **kwargs)
            else:
                self.numba_grid = RectilinearSGrid(
                    lon, lat, depth, time, mesh=mesh,
                    **kwargs)
        else:
            if depth is None or len(depth.shape) <= 1:
                self.numba_grid = CurvilinearZGrid(
                    lon, lat, depth, time, mesh=mesh,
                    **kwargs)
            else:
                self.numba_grid = CurvilinearSGrid(
                    lon, lat, depth, time, mesh=mesh,
                    **kwargs)

    @classmethod
    def wrap(cls, grid):
        return cls(grid=grid)

    def __getattr__(self, key):
        return getattr(self.numba_grid, key)
