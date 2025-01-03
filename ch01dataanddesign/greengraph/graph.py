
# sending requests to the web is not fully supported on jupyterlite yet, and the
# cells below might error out on the browser (jupyterlite) version of this notebook

# install geopy if it is not already installed
%pip install -q geopy

import numpy as np
import geopy
from matplotlib import pyplot as plt

from .map import Map


class Greengraph(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.geocoder = geopy.geocoders.Nominatim(user_agent="comp0023")

    def geolocate(self, place):
        return self.geocoder.geocode(place, exactly_one=False)[0][1]

    def location_sequence(self, start, end, steps):
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1], end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        """Count the amount of green space along a linear path between two locations."""
        self.steps = steps

        sequence = self.location_sequence(
            start=self.geolocate(self.start),
            end=self.geolocate(self.end),
            steps=steps,
        )
        maps = [Map(*location) for location in sequence]
        self.green_at_each_location = [current_map.count_green() for current_map in maps]

        return self.green_at_each_location

    def plot_green_between(self, steps):
        """ount the amount of green space along a linear path between two locations"""
        if not hasattr(self, 'green_at_each_location') or steps != self.steps:
            green_between_locations = self.green_between(steps)
        else:
            green_between_locations = self.green_at_each_location
        plt.plot(green_between_locations)
        xticks_steps = 5 if steps > 10 else 1
        plt.xticks(range(0, steps, xticks_steps))
        plt.xlabel("Sequence step")
        plt.ylabel(r"$N_{green}$")
        plt.title(f"{self.start} -- {self.end}")

