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


# A helper function for finding the highest stat (attribute)
def find_max_stat(stations: dict, stat: str) -> Tuple[str, int]:
    """ Goes through a dictionary of objects and finds wich one
    has the highest value of attribute 'stat'.  Returns a tuple in the form
    (object name, highest stat)

    Precondition: object has attribute 'name'
    Precondition: stat can be compared with '>'
    """
    max_stat = ('', -1)
    for station_key in stations:
        station = stations[station_key]
        # compare attributes and find the one with the higher value
        if getattr(station, stat) > max_stat[1]:
            max_stat = (station.name, getattr(station, stat))
        # if the values are the same choose the one that is first alphabetically
        elif getattr(station, stat) == max_stat[1]:
            if station.name < max_stat[0]:
                max_stat = (station.name, getattr(station, stat))
    return max_stat


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
        A list of rides in progress at a given time in the simulation
    ride_event_queue:
        A priority queue of ride events in simulation

    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]
    ride_event_queue: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.ride_event_queue = PriorityQueue()

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        # Add a ride start event for each ride
        for ride in self.all_rides:
            if start <= ride.start_time <= end:
                self.ride_event_queue.add(
                    RideStartEvent(self, ride.start_time, ride))
        step = timedelta(minutes=1)  # Each iteration spans one minute of time

        time = start
        while time < end:
            # If you want to use update_active_rides remember to
            #  change it right after the loop as well. #TODO : ASWELL
            self._update_active_rides_fast(time)
            # loop through station times and check if they are low unoccupied
            # or low on bikes, if they are in either situation, this is
            # registered. #TODO: FALAR QUE ESTAMOS INCREMENTANDO A VARIAVEL
            for station_key in self.all_stations:
                self.all_stations[station_key].enter_low_bike_time(
                    step.total_seconds())
                self.all_stations[station_key].enter_low_unoccupied_time(
                    step.total_seconds())
            # Send the list of all stations and bikes, with coordinates info
            #  to the visualizer #TODO: explain better
            self.visualizer.render_drawables(list(self.all_stations.values()) +
                                             self.active_rides,
                                             time)
            time += step
        # Count the bikes that leave and arrive at the last minute
        self._update_active_rides_fast(end)

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
            if ride.start_time <= time <= ride.end_time and\
                    ride not in self.active_rides:
                if ride.start.bike_successfully_departed():
                    self.active_rides.append(ride)
            elif time > ride.end_time or time < ride.start_time:
                if ride in self.active_rides:
                    self.active_rides.pop(self.active_rides.index(ride))
                    # This is where I update station statistic, bikes_arrived
                    ride.end.bike_arrival()

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
        #TODO: EXPLAIN EACH VARIABLE
        # Each temporary variable below stores a tuple containing their
        # respective information. Each variable is fed by its respective helper
        #function
        # -max_start refers to station which number of departures is greatest.
        max_start = find_max_stat(self.all_stations, 'bikes_left')
        # -max_end refers to station which number of arrivals is greatest.
        max_end = find_max_stat(self.all_stations, 'bikes_arrived')
        # -max_time_low_avialibility refers to the station which has the
        # greatest total amount of hours in low availability
        max_time_low_avialibility = find_max_stat(self.all_stations,
                                                  'low_bikes_counter')
        # -max_time_low_unoccupied refers to the station which has the
        # greatest total amount of hours in low ocupancy
        max_time_low_unoccupied = find_max_stat(self.all_stations,
                                                'low_unoccupied_counter')
        return {
            'max_start': max_start,
            'max_end': max_end,
            'max_time_low_availability': max_time_low_avialibility,
            'max_time_low_unoccupied': max_time_low_unoccupied
        }

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """
        while not self.ride_event_queue.is_empty():
            event = self.ride_event_queue.remove()
            if event.time > time:
                self.ride_event_queue.add(event)
                return

            new_events = event.process()
            for new_event in new_events:
                self.ride_event_queue.add(new_event)


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
        stations[s['n']] = Station((float(s['lo']), float(s['la'])),
                                   int(s['da']+s['ba']),
                                   int(s['da']),
                                   s['s'])

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
            if line[1] in stations and line[3] in stations:
                rides.append(Ride(stations[line[1]], stations[line[3]],
                                  (datetime.strptime(line[0],
                                                     DATETIME_FORMAT),
                                   datetime.strptime(line[2],
                                                     DATETIME_FORMAT))))
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
    """An event corresponding to the start of a ride.
    """
    ride: 'Ride'

    def __init__(self, simulation: 'Simulation', time: datetime,
                 ride: 'Ride') -> None:
        """Initialize a ride start event."""
        Event.__init__(self, simulation, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Adds a ride to the list of active rides
        and generates a ride ending event.
        """
        # Add ride to active
        if self.ride.start.bike_successfully_departed():
            self.simulation.active_rides.append(self.ride)
        # Create Ride end event
        ride_end = RideEndEvent(self.simulation, self.ride.end_time,
                                self.ride)
        return [ride_end]


class RideEndEvent(Event):
    """An event corresponding to the end of a ride."""
    ride: 'Ride'

    def __init__(self, simulation: 'Simulation', time: datetime,
                 ride: 'Ride') -> None:
        """Initialize a ride end event."""
        Event.__init__(self, simulation, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """ Removes ride from active rides."""
        self.ride.end.bike_arrival()
        self.simulation.active_rides.pop(
            self.simulation.active_rides.index(self.ride))
        # Returns an empty list of events so that the output from process is
        # consistent
        return []


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    # sim.run(datetime(2017, 6, 1, 8, 0, 0),
    #         datetime(2017, 6, 1, 9, 0, 0))
    sim.run(datetime(2017, 6, 1, 9, 30, 0),
            datetime(2017, 6, 1, 9, 40, 0))
    # Test for part one
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
        ]
    })
    print(sample_simulation())
