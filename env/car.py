class Car:
    def __init__(self, entry_time):
        self.entry_time = entry_time

    def __repr__(self):
        return "Car:(" + str(self.entry_time) + ")"

# we are keeping a track of entry time of vehicles to use is calculation of total waiting time later
