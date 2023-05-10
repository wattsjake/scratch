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
        self.valid_measure = []  # Whether or not the final measure is valid
        self.InitializeColumns()
        

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

        column = kwargs.get('column', self.column)   

        # Add measure if the measure is being forced
        if kwargs.get('force', False):
            self.__add_measure(*args, **kwargs)

        # Do not add the measure if measurements are not being taken
        if (not self.go_measure):
            return
        
        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = self.GetTimeIncrement(**kwargs)

        # If the delay has been met, add measure.  Otherwise, update the last measure so it is current.
        if (time_increment > self.delay):
            self.__add_measure(*args, **kwargs)
        else:
            self.__update_measure(*args)
            self.valid_measure[column] = False


    def __add_measure(self, *args, **kwargs):
        """Adds a measure to the current column of the data collector.

        Private method to be used within data collection class for measures that must be added.

        Args:
            measurement (data_class.Data): The measurement to be added.
        """        

        column = kwargs.get('column', self.column)
        
        if(self.valid_measure[column] == True):
            try:
                self.measures[column].append(args[0])
            except IndexError:
                self.measures[column].append(self.scale.get_weight_data())
            return
        
        # If the last measure in the column is not the final measure, update it and say it's the final measure
        self.__update_measure(*args, **kwargs)
        self.valid_measure = True
        

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


    def RemoveInvalidMeasures(self, **kwargs):
        r"""Removes measures that are not finalized from the data collector.

        Removes invalid measures from all columns by default.

        Args:
            **columns (int): Column to remove invalid measures from.
            **columns (list): List of columns to remove invalid measures from.

        """        

        columns = kwargs.get('columns', range(len(self.measures)))

        if columns is int:
            if self.valid_measure[columns] == False:
                self.measures[columns].pop()
            self.valid_measure[columns] = True

        for col in columns:
            if self.valid_measure[col] == False:
                self.measures[col].pop()
            self.valid_measure[col] = True


    def GetTimeIncrement(self, **kwargs):

        column = kwargs.get('column', self.column)

        # If the delay is based on the overall measures and there are enough measures to do so, return the overall delay
        if( (self.delay_overall or kwargs.get('overall', False)) and len(self.measures[column]) > (0 + self.valid_measure[column])):
            return (time.time() - self.start_times[column]) / len(self.measures[column])
        else:
            # Return the time since the last valid measure otherwise
            return time.time() - self.measures[column][-1 - self.valid_measure[column]].time


    def ExportData(self, file_out, **kwargs):

        self.RemoveInvalidMeasures()

        with open(file_out, 'w', newline='') as csvfile:
            fields = {}

            # Add the currently selected column if none is specified
            if kwargs.get("columns", None) == None:
                kwargs["columns"].insert(self.column)

            # Add fields for every column
            for column in kwargs["columns"]:
                if kwargs.get("times", False):
                    fields[self.TimeFieldName(column)] = None
                fields[self.MeasureFieldName(column)] = None

            # Create dictwriter object and write the header
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
            writer.writeheader()

            # Find max length of all columns
            max_length = 0
            for column in kwargs.get("columns"):
                if len(self.measures[column]) > max_length:
                    max_length = len(self.measures[column])

            
            # Write the data
            for row in range(max_length):
                writer_row = {}
                for column in kwargs.get("columns"):
                    if row < len(self.measures[column]):
                        if kwargs.get("times", False):
                            writer_row[self.TimeFieldName(column)] = (self.GetTimeSinceStart(column, row))
                        writer_row[self.MeasureFieldName(column)] = self.GetMeasure(column, row)
                    else:  # If there is no data for the row, write an empty string
                        if kwargs.get("times", False):
                            writer_row[self.TimeFieldName(column)] = ""
                        writer_row[self.MeasureFieldName(column)] = ""
                writer.writerow(writer_row)

            
    def TimeFieldName(self, column: int)-> str:
        return 'Time (' + self.measures[column][0].time_unit + ') ' + str(column)
    

    def GetTimeSinceStart(self, column: int, row: int):
        return self.measures[column][row].time - self.start_times[column]
    

    def MeasureFieldName(self, column: int)-> str:
        return 'Measure (' + self.measures[column][0].unit + ') ' + str(column)
    

    def GetMeasure(self, column: int, row: int):
        return self.measures[column][row].measure


    def ChangeColumn(self, column, **kwargs):

        # If forced, initialize all columns up to the specified column
        if kwargs.get('force', False):
            self.column = column
            self.InitializeColumns()
            return

        # If not forced and the column does not exist, raise an error
        if column >= len(self.measures):
            raise IndexError("Column does not exist")
        self.column = column


    def NextColumn(self):
        self.ChangeColumn(self.column + 1, force = True)


    def InitializeColumns(self, **kwargs):

        # If the column is not initialized, initialize it and all previous uninitialized columns
        while(len(self.measures) <= kwargs.get('column', self.column)):
            self.measures.append([None for y in range(0)])
            self.valid_measure.append(True)
        