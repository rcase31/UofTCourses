"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime
from typing import Tuple


# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (lat, long) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in lat/long coordinates
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station
    bikes_left: int
        the number of bikes that have left the station during the simulation
    bikes_arrived: int
        the number of bikes that have arrived at the station durning simulation
    low_bikes_counter: int
        tracks how long the station has 5 or less bikes
    low_unoccupied_counter: int
        tracks how long the station has 5 or less unoccupied spaces
    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    - 0 <= bikes_left
    - 0 <= bikes_arrived
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    bikes_left: int
    bikes_arrived: int
    low_bikes_counter: int
    low_unoccupied_counter: int

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.bikes_left = 0
        self.bikes_arrived = 0
        self.low_bikes_counter = 0
        self.low_unoccupied_counter = 0
        Drawable.__init__(self, STATION_SPRITE)

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location

    def bike_successfully_departed(self) -> bool:
        """Records that a bike left this station.
         returns True if their is a bike to depart and
         False if station is empty
         """ #TODO: THERE = THEIR
        if self.num_bikes > 0:
            print('wtf') #TODO: TAKE IT OUT
            self.bikes_left += 1
            self.num_bikes -= 1
            return True
        return False

    def bike_arrival(self) -> None:
        """Records that a bike arrived at this station"""
        if self.num_bikes < self.capacity:
            self.bikes_arrived += 1
            self.num_bikes += 1
#TODO: alterei o nome do metodo
    def enter_low_bike_time(self, time_step_seconds) -> None:
        """Updates the counter that
        keeps track of how long a station has 5 or less bikes
        """
        if self.num_bikes <= 5:
            self.low_bikes_counter += time_step_seconds

    def enter_low_unoccupied_time(self, time_step_seconds) -> None:
        """Updates the counter that
        keeps track of how long a station has 5 or less bikes
        """
        if (self.capacity - self.num_bikes) <= 5:
            self.low_unoccupied_counter += time_step_seconds


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]
        Drawable.__init__(self, RIDE_SPRITE)

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        # Get the amount of time elapsed since the bikes journey started
        current_time = (time - self.start_time).total_seconds()
        # Get the total time that will elapse in the bikes journey
        total_time = (self.end_time - self.start_time).total_seconds()
        # Get the longitudinal distance the bike will travel
        lon_distance = (self.end.location[0] - self.start.location[0])
        # Get the latitudinal distance the bike will travel
        lat_distance = (self.end.location[1] - self.start.location[1])
        # the lon and lat positions will be equal to
        # the entire distance * the fraction  of time elapsed
        # + starting position
        return (current_time*lon_distance/total_time + self.start.location[0],
                current_time*lat_distance/total_time + self.start.location[1])


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
