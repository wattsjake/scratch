import time
import csv

class DataCollect:

    def __init__(self, **kwargs):
        self.unit = kwargs.get('unit', 'g')
        self.time_unit = kwargs.get('time_unit', 's')
        self.delay = kwargs.get('delay', 0.5)
        self.delay_overall = kwargs.get('delay_type', False)
        self.measures = []
        self.times = []
        self.go_measure = False

    def StartMeasure(self):
        self.go_measure = True
        self.times.append(0)
        self.measures.append(self.scale.read_screen().decode('utf-8'))
        self.start_time = time.time()
        self.last_time = self.start_time

    def StopMeasure(self):
        self.go_measure = False

    def GetMeasure(self, **kwargs):

        # Get the time increment. If delay_overall is true, get the overall delay based on the number of measures.
        # Otherwise, get the delay since the last measure.
        time_increment = None
        if(self.delay_overall):
            time_increment = (time.time() - self.start_time) / len(self.measures)
        else:
            time_increment = time.time() - self.last_time

        # If you have the flag to measure and the delay has been met, get the next measure
        if (self.go_measure and (time.time() - self.last_time < self.delay)) or kwargs.get('force', False):
            self.measures.append(self.scale.read_screen().decode('utf-8'))
            self.times.append(time.time() - self.start_time)

    