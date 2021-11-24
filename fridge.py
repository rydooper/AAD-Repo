
class OpenDoorError(Exception):
    def __init__(self):
        super(OpenDoorError, self).__init__("Door could not be opened, please close the other fridge door")


class Fridge:

    def __init__(self):
        self.front_door_open: bool = False
        self.back_door_open: bool = False

    def check_both_doors_open(self):  # Runs Checks to ensure both doors aren't open, even in the event of a bug
        if self.front_door_open and self.back_door_open:
            self.front_door_open = False
            self.back_door_open = False
            raise OpenDoorError

    def open_front_door(self):
        if not self.back_door_open:
            self.front_door_open = True
        self.check_both_doors_open()

    def open_back_door(self):
        if not self.front_door_open:
            self.back_door_open = True
        self.check_both_doors_open()


def addition(i) -> int:
    return i+5
