"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

#Function constants for reporting beggining and ending of rides
RIDE_BEGUN = True
RIDE_FINISHED = False
# Stock issues report
SUCCESSFUL_REPORT = 0
EMPTY_STATION_ISSUE = 1
FULL_STATION_ISSUE = 2

class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    active_rides:
        All rides that are active during simulation
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.visualizer = Visualizer()
        self.active_rides = []

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time
        current_time = start
        while current_time <= end:
            self._update_active_rides(current_time)
            # Method that draws all stations and bikes on the map
            self.visualizer.render_drawables(list(self.all_stations.values())\
                                             + self.active_rides, current_time)
            current_time += step

        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.
        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.
        """
        for ride in self.all_rides:
            # Check whether the current time is between start and end
            if time > ride.start_time and time < ride.end_time:
                # Check whether it is already in the active rides list
                if not ride in self.active_rides:
                    # Reports that this ride has just begun
                    # this method will also lead to an update on station's bike
                    # number.
                    if ride.report_status(RIDE_BEGUN, time) \
                            == SUCCESSFUL_REPORT:
                        # Adds to the active rides list if no anomaly was
                        # detected
                        self.active_rides.append(ride)
            else:
                if ride in self.active_rides:
                    # Reports that this ride has finished
                    # this method will also lead to an update on station's bike
                    # number
                    ride.report_status(RIDE_FINISHED, time)
                    # If a finished or not yet beginned ride is in this
                    #  list, removes it.
                    self.active_rides.remove(ride)

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """

        max_start = ('', -1)
        max_end = ('', -1)
        max_time_low_availability = ('', -1)
        max_time_low_unoccupied = ('', -1)

        for station_key in self.all_stations:
            station = self.all_stations[station_key]
            #TODO helper function
            if station.bikes_left > max_start[1]:
                max_start = (station.name, station.bikes_left)
            if station.bikes_arrived > max_end[1]:
                max_end = (station.name, station.bikes_arrived)
            if station.max_time_low_bikes > max_time_low_availability[1]:
                max_time_low_availability = (station.name,
                                             station.max_time_low_bikes)
            if station.max_time_low_unoccupied > max_time_low_unoccupied[1]:
                max_time_low_unoccupied = (station.name,
                                           station.max_time_low_unoccupied)


        return {
            'max_start': max_start,
            'max_end': max_end,
            'max_time_low_availability': max_time_low_availability,
            'max_time_low_unoccupied': max_time_low_unoccupied
        }

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """
        pass


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """
    # Read in raw data using the json library.
    with open(stations_file) as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().
        # Inputs for Station Class (with keys from dictionary) :
        #   -Lon/Lat  (lo/la)
        #   -Capacity (da + ba)
        #   -Number of bikes (da)
        #   -Name (s)
        station = Station((s['lo'], s['la']), s['da'] + s['ba'],\
                          s['da'], s['s'])
        stations[s['n']] = station

    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        for line in csv.reader(file):
            # line is a list of strings, following the format described
            # in the assignment handout.
            #
            # Convert between a string and a datetime object
            # using the function datetime.strptime and the DATETIME_FORMAT
            # constant we defined above. Example:
            # >>> datetime.strptime('2017-06-01 8:00', DATETIME_FORMAT)
            # datetime.datetime(2017, 6, 1, 8, 0)
            # CSV Columns:
            #   -Start time [0]
            #   -Start station code [1]
            #   -End time  [2]
            #   -End station code [3]
            #   -ignore the rest [4,5]
            # Ride class inputs:
            #   -Start station (Station())
            #   -End station (Station())
            #   -Times (Tuple(start,end))
            start_station_code = line[1]
            end_station_code = line[3]
            # First check whether the stations from the ride are present in the
            # stations registry
            if start_station_code and end_station_code in stations:
                start_time = datetime.strptime(line[0], DATETIME_FORMAT)
                end_time = datetime.strptime(line[2], DATETIME_FORMAT)
                start_station = stations[start_station_code]
                end_station = stations[end_station_code]
                ride = Ride(start_station, end_station, (start_time, end_time))
                rides.append(ride)

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride."""
    pass


class RideEndEvent(Event):
    """An event corresponding to the start of a ride."""
    pass


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0),
            datetime(2017, 6, 1, 9, 0, 0))

    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    import python_ta
    python_ta.check_all(config={
         'allowed-io': ['create_stations', 'create_rides'],
         'allowed-import-modules': [
             'doctest', 'python_ta', 'typing',
             'csv', 'datetime', 'json',
             'bikeshare', 'container', 'visualizer'
         ]})
    print(sample_simulation())
