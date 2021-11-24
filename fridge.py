
class OpenDoorError(Exception):
    def __init__(self):
        super(OpenDoorError, self).__init__("Door could not be open, please close the other fridge door")


class Fridge:

    def __init__(self):
        self.front_door_open = False
        self.back_door_open = False

    def open_front_door(self):
        if not self.back_door_open:
            self.front_door_open = True
        else:
            raise OpenDoorError

    def open_back_door(self):
        if not self.front_door_open:
            self.back_door_open = True
        else:
            raise OpenDoorError


def addition(i):
    return i+5


print(addition(6))
