import math
from io import BytesIO

import numpy as np
import imageio.v3 as iio

# sending requests to the web is not fully supported on jupyterlite yet, and the
# cells below might error out on the browser (jupyterlite) version of this notebook
import requests

class Map(object):
    def __init__(self, latitude, longitude, satellite=True, zoom=10,
                 sensor=False):
        base = "https://mt0.google.com/vt?"
        x_coord, y_coord = self.deg2num(latitude, longitude, zoom)

        params = dict(
            x=x_coord,
            y=y_coord,
            z=zoom,
        )
        if satellite:
            params['lyrs'] = 's'

        self.image = requests.get(
            base, params=params).content  # Fetch our PNG image data
        content = BytesIO(self.image)
        self.pixels = iio.imread(content) # Parse our PNG image as a numpy array

    def deg2num(self, latitude, longitude, zoom):
        """Convert latitude and longitude to XY tiles coordinates."""

        lat_rad = math.radians(latitude)
        n = 2.0 ** zoom
        x_tiles_coord = int((longitude + 180.0) / 360.0 * n)
        y_tiles_coord = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)

        return (x_tiles_coord, y_tiles_coord)

    def green(self, threshold):
        """Determine if each pixel in an image array is green."""

        # RGB indices
        red, green, blue = range(3)

        # Use NumPy to build an element-by-element logical array
        greener_than_red = self.pixels[:, :, green] > threshold * self.pixels[:, :, red]
        greener_than_blue = self.pixels[:, :, green] > threshold * self.pixels[:, :, blue]
        green = np.logical_and(greener_than_red, greener_than_blue)
        return green

    def count_green(self, threshold=1.1):
        return np.sum(self.green(threshold))

    def show_green(data, threshold=1.1):
        green = self.green(threshold)
        out = green[:, :, np.newaxis] * array([0, 1, 0])[np.newaxis, np.newaxis, :]
        buffer = BytesIO()
        result = iio.imwrite(buffer, out, extension='.png')
        return buffer.getvalue()
