import time
import csv

class DataCollect:

    def __init__(self, **kwargs):
        self.unit = kwargs.get('unit', 'g')
        self.time_unit = kwargs.get('time_unit', 's')
        self.delay = kwargs.get('delay', 0.5)
        self.delay_overall = kwargs.get('delay_type', True)
        self.measures = []
        self.times = []
        self.go_measure = False
        self.start_time = None
        self.last_time = None

    def StartMeasure(self, measurement):
        self.go_measure = True
        if self.start_time == None:
            self.start_time = time.time()
        self.times.append(time.time() - self.start_time)
        self.measures.append(measurement)
        self.last_time = self.start_time
        

    def StopMeasure(self):
        self.go_measure = False

    def AddMeasure(self, measurement, **kwargs):

        if not self.go_measure:
            return
        
        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = self.GetTimeIncrement()

        # If the delay has been met or a measure is being forced, add measure.
        if (time_increment > self.delay) or kwargs.get('force', False):
            self.times.append(time.time() - self.start_time)
            self.measures.append(measurement)
            self.last_time = time.time()

    def GetTimeIncrement(self, **kwargs):
        time_increment = 0
        if( (self.delay_overall or kwargs.get('overall', False)) and len(self.measures) > 0):
            return (time.time() - self.start_time) / len(self.measures)
        else:
            return time.time() - self.last_time

    def ExportData(self, file_out, **kwargs):
        with open(file_out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Time (' + self.time_unit + ')', 'Weight (' + self.unit + ')'])
            for i in range(len(self.measures)):
                writer.writerow([self.times[i], self.measures[i]])