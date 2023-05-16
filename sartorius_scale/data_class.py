import time
import csv
from dataclasses import dataclass
import numpy as np
from scaledrivers.scale import Scale


@dataclass
class Data:
    r"""Stores data for a given measurement.

    Defaults:
        time: float = time.time()
        measure: float = 0
        unit: str = 'g'  # Default unit is grams
        time_unit: str = 's'  # Default time unit is seconds
        stable: bool = False
    """    

    def __init__(self):
        r"""Sets time to the current time when the object was created.
        """
        self.time = time.time()

    time: float  # Time is automatically set to when the object was created
    measure: float = 0
    unit: str = 'g'  # Default unit is grams
    time_unit: str = 's'  # Default time unit is seconds
    stable: bool = False




class DataCollect:
    r"""Collects Data objects and stores them in columns and rows.
    """    

    def __init__(self, **kwargs):
        r"""Creates default values for the data collector.

        Args:
            **delay (float, optional): Delay between measures. Default is 0.5.
            **delay_overall (bool, optional): Whether or not the delay is overall or between measures. Default is True.
            **scale (Scale, optional): The scale to be used for data collection.
        """        

        self.delay = kwargs.get('delay', 0.5)
        self.delay_overall = kwargs.get('delay_overall', True)
        self.measures = [[None for x in range(0)] for y in range(0)]  # Uses Data class for storing measures, stores lists of measures for each column
        self.go_measure = False
        self.column = 0  # Which column data is being collected in
        self.scale = kwargs.get('scale', None)
        self.valid_measure = []  # Whether or not the final measure is valid
        self.InitializeColumns()
        

    def set_scale(self, scale: Scale):
        r"""Sets the scale for the data collector.

        Args:
            scale (Scale): The scale to be used for data collection.
        """        

        self.scale = scale


    def StartMeasure(self, *args):
        r"""Start measuring data.

        Allows data to be collected at regular intervals from the start time
        without being forced.  Initial measurement is required if there is no
        scale to get the initial measurement from.

        Args:
            *args[0] (Data, optional): Initial measurement to be added. If Data Collector has scale, default is measurement from scale.
        """      

        # If not currently measuring, start measuring  
        if not self.go_measure:
            self.go_measure = True
            self.AddMeasure(*args, force = True)
        

    def StopMeasure(self):
        """Stop measuring data.

        Forced measures are still allowed.
        """        

        self.go_measure = False


    def AddMeasure(self, *args, **kwargs):
        r"""Adds a measure to the current column of the data collector.

        Adds a measure to the current column of the data collector if the delay has been met
        or if the measure is being forced.  If the delay has not been met, the measure is not added.
        A measurement must be included if there is no scale to take the measurement from.

        Args:
            *args[0] (Data, optional): The measurement to be added. If Data Collector has scale, default is measurement from scale.
            **force (bool, optional): Whether or not the measure is being forced. Default is False.
            **column (int, optional): Which column the measure is being added to. Default is current column.
        """     

        column = kwargs.get('column', self.column)   

        # Add measure if the measure is being forced
        if kwargs.get('force', False):
            self.__add_measure(*args, **kwargs)
            self.valid_measure[column] = True
            return

        # Do not add the measure if measurements are not being taken
        if (not self.go_measure):
            return

        # If the last measure was valid, add a new one. If not, update the last one
        if (self.valid_measure[column]):
            self.__add_measure(*args, **kwargs)
        else:
            self.__update_measure(*args)

        # If the delay was met, set the last measure to be valid
        self.valid_measure[column] = self.GetTimeIncrement(**kwargs) > self.delay


    def __add_measure(self, *args, **kwargs):
        r"""Adds a measure to the current column of the data collector.

        Private method to be used within data collection class for measures that must be added.

        Args:
            *args[0] (Data, optional): The measurement to be added. If Data Collector has scale, default is measurement from scale.
            **column (int, optional): Which column the measure is being added to. Default is current column.
        """        

        column = kwargs.get('column', self.column)
        
        if(self.valid_measure[column]):
            try:
                self.measures[column].append(args[0])
            except IndexError:
                self.measures[column].append(self.scale.get_weight_data())
            return
        
        # If the last measure in the column is not the final measure, update it and say it's the final measure
        self.__update_measure(*args, **kwargs, row = -1)
        self.valid_measure[column] = True
        

    def __update_measure(self, *args, **kwargs):
        r"""Updates a measure in the current column of the data collector.

        Private method to be used within data collection class for measures that must be updated.

        Args:
            *args[0] (Data, optional): The measurement to replace another measurement. If Data Collector has scale, default is measurement from scale.
            **column (int, optional): Which column the measure is being added to. Defaults to current column.
            **row (int, optional): Which row the measure is being updated at. Defaults to last row.
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
            **columns (int, optional): Column to remove invalid measures from.
            **columns (list, optional): List of columns to remove invalid measures from. Defaults to all columns.

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
        r"""Gets the time increment to find delay.

        Gets the time increment to find delay based on the delay type.
        Overall delay is the number of measures in the column divided by the time between first and last measures.
        Not overall delay is the time between the last two measures.

        Args:
            **column (int, optional): Column to get time increment for. Defaults to current column.
            **overall (bool, optional): Whether or not to get the overall delay. Defaults to delay_overall.

        Returns:
            float: Delay for given delay type.
        """        

        column = kwargs.get('column', self.column)

        # If the delay is based on the overall measures and there are enough measures to do so, return the overall delay
        if (self.delay_overall or kwargs.get('overall', False)):
            return (self.GetTimeSinceStart(column)) / self.GetValidLength()
        else:
            # Return the time since the last valid measure otherwise
            return time.time() - self.measures[column][-1 - int(self.valid_measure[column] == False)].time  # Do most recent measure if it is valid


    def ExportData(self, file_out: str, **kwargs):
        r"""Exports measurement data to a csv file.

        Args:
            file_out (str): Name of file to output data to.
            **columns (list, optional): Ordered list of columns to export. Defaults to all columns.
            **times (bool, optional): Whether or not to include time data. Defaults to False.
        """        

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

            
    def TimeFieldName(self, column: int = None) -> str:
        r"""Gets the time field name for a given column.

        Args:
            column (int, optional): Column to get time field name for. Defaults to current column.

        Returns:
            str: Time field name for given column.
        """        

        if column == None:
            column = self.column

        return 'Time (' + self.measures[column][0].time_unit + ') ' + str(column)


    def GetStartTime(self, column: int = None) -> float:
        r"""Gets the start time for a given column.

        Args:
            column (int, optional): Column to get start time for. Defaults to current column.

        Returns:
            float: Start time for given column.
        """        

        if column == None:
            column = self.column

        return self.measures[column][0].time
    

    def GetTimeSinceStart(self, column: int = None, row: int = -1) -> float:
        r"""Gets the time of a data point from the start of the column.

        Args:
            column (int, optional): Which column to pull data from. Defaults to current column.
            row (int, optional): Which row of the column to compare to first item in column. Defaults to last row of column.

        Returns:
            float: Time between selected measure and first measure in column
        """        

        if column == None:
            column = self.column

        return self.measures[column][row].time - self.GetStartTime(column)
    

    def MeasureFieldName(self, column: int = None) -> str:
        r"""Gets the measure field name for a given column.

        Args:
            column (int, optional): Column to get measure field name from. Defaults to current column.

        Returns:
            str: Measure field name for given column.
        """        

        if column == None:
            column = self.column

        return 'Measure (' + self.measures[column][0].unit + ') ' + str(column)
    

    def GetMeasure(self, column: int = None, row: int = -1) -> float:
        r"""Gets the measurement of a data point from a given column and row.

        Args:
            column (int, optional): Which column to pull data from. Defaults to current column.
            row (int, optional): Which row of the column to pull data from. Defaults to last row.

        Returns:
            float: Measurement of selected datum.
        """        
        
        if column == None:
            column = self.column

        return self.measures[column][row].measure


    def GetValidLength(self, column: int = None) -> int:
        r"""Gets the number of valid measurements in a given column.

        Args:
            column (int, optional): Column to get valid length of. Defaults to current column.

        Returns:
            int: Number of valid measurements in column.
        """        

        if column == None:
            column = self.column

        return len(self.measures[column]) - int(self.valid_measure[column] == False)


    def ChangeColumn(self, column: int, **kwargs):
        r"""Changes the column to a specified column.

        Args:
            column (int): Column to move to.
            **force (bool, optional): Whether or not to force the selected column to exist. Defaults to False.

        Raises:
            IndexError: Moved to column that does not exist.
        """        

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
        r"""Moves to the next column from the currently selected column.
        """        
        self.ChangeColumn(self.column + 1, force = True)


    def InitializeColumns(self, **kwargs):
        r"""Initializes columns up to the currently selected column.

        Args:
            **column (int): Column to initialize up to. Defaults to current column.
        """        

        # If the column is not initialized, initialize it and all previous uninitialized columns
        while(len(self.measures) <= kwargs.get('column', self.column)):
            self.measures.append([None for y in range(0)])
            self.valid_measure.append(True)
        