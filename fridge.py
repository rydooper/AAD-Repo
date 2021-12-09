from custom_exceptions import OpenDoorError


class Fridge:

    __slots__ = ["front_door_open", "back_door_open", "max_capacity"]

    def __init__(self, capacity):
        self.max_capacity: int = capacity
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
