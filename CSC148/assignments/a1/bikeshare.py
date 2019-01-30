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

# Function Constants
# Station Stock control
COUNT_DOWN = False
COUNT_UP = True
# Stock issues report
SUCCESSFUL_REPORT = 0
EMPTY_STATION_ISSUE = 1
FULL_STATION_ISSUE = 2
STOCK_UPDATE_OK = True
STOCK_UPDATE_FAIL = False
# Stats report headers (for registry dictionary)
NUMBER_OF_BIKES = 'bike_num'
TIME = 'time'
DEPARTURES = 'departures'
ARRIVALS = 'arrivals'
TIME_LOW_AVAILABILITY = 'low'
TIME_HIGH_AVAILABILITY = 'high'
TIME_ELAPSED = 'time_elapsed'


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
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in long/lat coordinates
        **UPDATED**: make sure the first coordinate is the longitude,
        and the second coordinate is the latitude.
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station
    simulation_stat: dict
        this dictionary works like a table, where each registred attribute
        is a reference to their elements.
    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    simulation_stat: dict
    _simulated: bool

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        Drawable.__init__(self, STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.simulation_stat = {NUMBER_OF_BIKES: [],
                                TIME: [], DEPARTURES: [],
                                ARRIVALS: [], TIME_ELAPSED: []}
        self._simulated = False

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location

    def feed_stats(self, time: datetime, begun: bool) -> None:
        """Register the amount of bikes in this station at a given time
        """
        self.simulation_stat[NUMBER_OF_BIKES].append(self.num_bikes)
        self.simulation_stat[TIME].append(time)
        self.simulation_stat[DEPARTURES].append(begun)
        self.simulation_stat[ARRIVALS].append(not begun)

    def get_simulation_variable(self, registry_type: str) -> int:
        """Returns the appropriate value, from the operation associated8
        with the registry type.
        """
        with self.simulation_stat[registry_type] as stat:
            if registry_type == DEPARTURES or DEPARTURES:
                return sum(stat)
            elif registry_type == NUMBER_OF_BIKES:
                return max(stat)
            else:
                return 0

    def get_simulation_time_availability(self, sim_begin_time: datetime,
                                         sim_end_time: datetime) \
            -> (datetime, datetime):
        """Returns the amount of time a station has remained on low or high
         availability."""

        # Calls a 'private' method that creates the time deltas between time
        # stamps. This method need only to be called once.
        if not self._simulated:
            self._create_timedelta_entries(sim_begin_time, sim_end_time)
            self._simulated = True

        # Loops through each register, considering the number of bikes at each
        # time period. After this loop the total amount of time that a station
        # spent with low and high availability should be fed into the
        # 'time information' tuple.
        time_information = (0, 0)
        for i in range(len(self.simulation_stat[TIME_ELAPSED])):
            if self.simulation_stat[NUMBER_OF_BIKES][i] > 5:
                time_information[0] += self.simulation_stat[TIME_ELAPSED][i]
            elif self.simulation_stat[NUMBER_OF_BIKES][i] < 5:
                time_information[1] += self.simulation_stat[TIME_ELAPSED][i]

        return time_information

    def successful_update_bike_number(self, bike_incoming: bool) -> bool:
        """Updates when a bike leaves or returns to this station
        If bike_incoming is True, then a bike just arrived to the station
        If bike_incoming is False, then a bike just left the station
        """
        if bike_incoming:
            if self.num_bikes < self.capacity:
                self.num_bikes += 1
                return STOCK_UPDATE_OK
            else:
                return STOCK_UPDATE_FAIL
        elif self.num_bikes > 0:
            # This also checks if there is any bike in stock, prior to
            # decreasing station's number
            self.num_bikes -= 1
            return STOCK_UPDATE_OK
        else:
            return STOCK_UPDATE_FAIL

    def _create_timedelta_entries(self, sim_end_time: datetime,
                                  sim_begin_time: datetime) -> None:
        # This segment of code creates the TIME_ELAPSED list for the
        # simulation_stat attribute in each Station

        # Erases any previous registry in this dictionary
        # (this is just a safety measure, since this method will only  be
        # called once)
        self.simulation_stat[TIME_ELAPSED] = []

        # This segment of code creates a new temporary vector containing
        # start and end time of simulation
        with self.simulation_stat[TIME] as time_vec:
            # copy the time vector
            temp_vec = [time_vec[i] for i in range(len(time_vec))]
            temp_vec.append(sim_end_time)
            temp_vec.insert(0, sim_begin_time)

        # This segment of code calculates the time deltas for each period
        # of time
        self.simulation_stat[TIME_ELAPSED] = [temp_vec[i + 1] - temp_vec[i] \
                                              for i in range(len(temp_vec) - 1)]


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
        Drawable.__init__(self, RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        current_time = (time - self.start_time).total_seconds()
        total_time = (self.end_time - self.start_time).total_seconds()
        lon_distance = (self.end.location[0] - self.start.location[0])
        lat_distance = (self.end.location[1] - self.start.location[1])
        return (current_time*lon_distance/total_time + self.start.location[0],
                current_time*lat_distance/total_time + self.start.location[1])

    def report_status(self, begun: bool, time: datetime) -> int:
        """This method is reports to the station when a bike has departed from
        it, or has arrived on it.
        When begun is True, it is because it has departed from its origin
        station. But when it is False, this means it has arrived on its
        destination.
        """

        start_station = self.start
        end_station = self.end

        if begun:
            if start_station.successful_update_bike_number(COUNT_DOWN):
                start_station.feed_stats(time, begun)
                return SUCCESSFUL_REPORT
            else:
                return EMPTY_STATION_ISSUE
        else:
            if end_station.successful_update_bike_number(COUNT_UP):
                end_station.feed_stats(time, begun)
                return SUCCESSFUL_REPORT
            else:
                return FULL_STATION_ISSUE


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
