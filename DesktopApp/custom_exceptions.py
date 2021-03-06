class RoleError(Exception):

    def __init__(self):
        super(RoleError, self).__init__("Role could not be assigned")


class OpenDoorError(Exception):
    def __init__(self):
        super(OpenDoorError, self).__init__("Door could not be opened, please close the other fridge door")
