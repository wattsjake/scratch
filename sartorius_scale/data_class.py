import time
import csv
import copy
from dataclasses import dataclass
import numpy as np
from scale_superclass import Scale


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
        self.scale = kwargs.get('scale', None)
        self.final_measure = []  # Whether or not the final measure has been taken
        self.__initialize_columns()
        

    def set_scale(self, scale: Scale):
        """Sets the scale for the data collector.

        Args:
            scale (Scale): The scale to be used for data collection.
        """        

        self.scale = scale


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


    def AddMeasure(self, *args, **kwargs):
        """Adds a measure to the current column of the data collector.

        Adds a measure to the current column of the data collector if the delay has been met
        or if the measure is being forced.  If the delay has not been met, the measure is not added.

        Args:
            measurement (Data): Measurement to be added.
        """        

        # Add measure if the measure is being forced
        if kwargs.get('force', False):
            self.__add_measure(*args)

        # Do not add the measure if measurements are not being taken
        if (not self.go_measure):
            return
        
        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = self.GetTimeIncrement()

        # If the delay has been met, add measure.
        if (time_increment > self.delay):
            self.__add_measure(*args)


    def __add_measure(self, *args, **kwargs):
        """Adds a measure to the current column of the data collector.

        Private method to be used within data collection class for measures that must be added.

        Args:
            measurement (data_class.Data): The measurement to be added.
        """        

        column = kwargs.get('column', self.column)
        
        if(self.final_measure[column] == True):
            try:
                self.measures[column].append(args[0])
            except IndexError:
                self.measures[column].append(self.scale.get_weight_data())
            return
        
        # If the last measure in the column is not the final measure, update it and say it's the final measure
        self.__update_measure(*args, **kwargs)
        self.final_measure = True
        

    def __update_measure(self, *args, **kwargs):
        """Updates a measure in the current column of the data collector.

        Private method to be used within data collection class for measures that must be updated.
        """        

        column = kwargs.get('column', self.column)
        row = kwargs.get('row', -1)

        try:
            self.measures[column][row] = args[0]
        except IndexError:
            self.measures[column][row] = self.scale.get_weight_data()


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

            # Create dictwriter object and write the header
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

    def ChangeColumn(self, column, **kwargs):

        # If forced, initialize all columns up to the specified column
        if kwargs.get('force', False):
            self.column = column
            self.__initialize_columns()
            return

        # If not forced and the column does not exist, raise an error
        if column >= len(self.measures):
            raise IndexError("Column does not exist")
        self.column = column

    def NextColumn(self):
        self.ChangeColumn(self.column + 1, force = True)

    def __initialize_columns(self, **kwargs):

        # If the column is not initialized, initialize it and all previous uninitialized columns
        while(len(self.measures) <= kwargs.get('column', self.column)):
            self.measures.append([None for y in range(0)])
            self.final_measure.append(True)
        