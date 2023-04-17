import time
import csv
from dataclasses import dataclass


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
        self.measures = [[]]  # Uses Data class for storing measures
        self.go_measure = False
        self.start_times = []
        self.column = 0  # Which column data is being collected in

    def StartMeasure(self, measurement):
        if not self.go_measure:
            self.go_measure = True

            # If the start time is not set, set it
            if len(self.start_times) == self.column:
                self.start_times.append(time.time())
            self.AddMeasure(measurement, force = True)
        

    def StopMeasure(self):
        self.go_measure = False

    def AddMeasure(self, measurement, **kwargs):

        # Add measure if the measure is being forced
        if kwargs.get('force', False):
            self.measures[self.column].append(measurement)
            return

        # Do not add the measure if measurements are not being taken
        if (not self.go_measure):
            return
        
        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = self.GetTimeIncrement()

        # If the delay has been met, add measure.
        if (time_increment > self.delay):
            self.measures[self.column].append(measurement)

    def GetTimeIncrement(self, **kwargs):
        time_increment = 0
        if( (self.delay_overall or kwargs.get('overall', False)) and len(self.measures[self.column]) > 0):
            return (time.time() - self.start_times[self.column]) / len(self.measures[self.column])
        else:
            return time.time() - self.measures[self.column][-1].time

    def ExportData(self, file_out, **kwargs):
        with open(file_out, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',')
            fields = []

            # Add the currently selected column if none is specified
            if kwargs.get("columns", None) == None:
                kwargs["columns"].insert(self.column)

            # Write the header, including times if indicated
            for column in kwargs["columns"]:
                if kwargs["times"]:
                    fields.append('Time (' + self.measures[column][0].time_unit + ') ' + str(column))
                fields.append('Measure (' + self.measures[column][0].unit + ') ' + str(column))
            writer.writeheader(fields)

            # Find the maximum length of the columns
            max_len = 0
            for column in kwargs.get("columns"):
                max_len = max(max_len, len(self.measures[column]))

            # Write the data
            for i in range(max_len):
                row = {}
                for column in kwargs.get("columns"):
                    if i < len(self.measures[column]):
                        if kwargs.get("times", True):
                            row['Time (' + self.measures[column][0].time_unit + ') ' + str(column)] = (self.measures[column][i].time - self.start_time[column])
                        row['Measure (' + self.measures[column][0].unit + ') ' + str(column)] = self.measures[column][i].measure
                writer.writerow(row)

    def ChangeColumn(self, column):
        self.column = column
        self.StopMeasure()

    def NextColumn(self):
        self.ChangeColumn(self.column + 1)