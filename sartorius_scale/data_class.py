import time
import csv
from dataclasses import dataclass
import numpy as np
from numpy_da import DynamicArray


@dataclass
class Data:
    measure: float = 0
    time: float = time.time()
    unit: str = 'g'
    time_unit: str = 's'
    stable: bool = False


class DataCollect:

    def __init__(self, **kwargs):
        self.delay = kwargs.get('delay', 0.5)
        self.delay_overall = kwargs.get('delay_type', True)
        self.measures = [[None for x in range(0)] for y in range(0)]  # Uses Data class for storing measures, stores lists of measures for each column
        self.go_measure = False
        self.start_times = []  # Start times for each column
        self.indexes = []  # Indexes for each column
        self.column = 0  # Which column data is being collected in

    def StartMeasure(self, measurement: Data):
        """Start measuring data.

        Allows data to be collected at regular intervals from the start time
        without being forced.

        Args:
            measurement (Data): Initial measurment to be added.
        """      

        # If not currently measuring, start measuring  
        if not self.go_measure:
            self.go_measure = True

            # If the start time is not set, set it
            if len(self.start_times) == self.column:
                self.start_times.append(time.time())
            self.AddMeasure(measurement, force = True)
        

    def StopMeasure(self):
        """Stop measuring data.

        Forced measures are still allowed.
        """        

        self.go_measure = False

    def AddMeasure(self, measurement: Data, **kwargs):
        """Adds a measure to the current column of the data collector.

        Adds a measure to the current column of the data collector if the delay has been met
        or if the measure is being forced.  If the delay has not been met, the measure is not added.

        Args:
            measurement (Data): Measurement to be added.
        """        

        # Add measure if the measure is being forced
        if kwargs.get('force', False):
            self.__add_measure(measurement)
            return

        # Do not add the measure if measurements are not being taken
        if (not self.go_measure):
            return
        
        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = self.GetTimeIncrement()

        # If the delay has been met, add measure.
        if (time_increment > self.delay):
            self.__add_measure(measurement)


    def __add_measure(self, measurement: Data):
        """Adds a measure to the current column of the data collector.

        Private method to be used within data collection class for measures that must be added.
        Creates a new column if the current column is not initialized.

        Args:
            measurement (data_class.Data): The measurement to be added.
        """        

        # If the column is not initialized, initialize it
        if( len(self.measures) <= self.column):
            self.measures.append([None for y in range(0)])
        self.measures[self.column].append(measurement)

    def GetTimeIncrement(self, **kwargs):
        time_increment = 0
        if( (self.delay_overall or kwargs.get('overall', False)) and len(self.measures[self.column]) > 0):
            return (time.time() - self.start_times[self.column]) / len(self.measures[self.column])
        else:
            return time.time() - self.measures[self.column][-1].time

    def ExportData(self, file_out, **kwargs):
        with open(file_out, 'w', newline='') as csvfile:
            fields = {}

            # Add the currently selected column if none is specified
            if kwargs.get("columns", None) == None:
                kwargs["columns"].insert(self.column)

            # Add fields for every column
            for column in kwargs["columns"]:
                if kwargs.get("times", False):
                    fields['Time (' + self.measures[column][0].time_unit + ') ' + str(column)] = None
                fields['Measure (' + self.measures[column][0].unit + ') ' + str(column)] = None

            # Create dictwriter object and write header
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
            writer.writeheader()

            # Find the maximum length of the columns
            max_len = 0
            for column in kwargs.get("columns"):
                max_len = max(max_len, len(self.measures[column]))

            # Write the data
            for i in range(max_len):
                row = {}
                for column in kwargs.get("columns"):
                    if i < len(self.measures[column]):
                        if kwargs.get("times", False):
                            row['Time (' + self.measures[column][0].time_unit + ') ' + str(column)] = (self.measures[column][i].time - self.start_times[column])
                        row['Measure (' + self.measures[column][0].unit + ') ' + str(column)] = self.measures[column][i].measure
                writer.writerow(row)

    def ChangeColumn(self, column):
        self.column = column
        self.StopMeasure()

    def NextColumn(self):
        if len(self.measures) < self.column + 1:
            self.measures = np.append(self.measures, np.ndarray((1, 20), dtype=Data))
        self.ChangeColumn(self.column + 1)