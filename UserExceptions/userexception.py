# class MyError is extended from super class Exception
class exception_device_not_found(Exception):
    def __init__(self, message):
        self.message = message
        try:
            raise (exception_device_not_found("The device in exception is not found"))
            # Value of Exception is stored in error
        except exception_device_not_found as error:
            print('A New Exception occured:', error)


class Instance_Not_Available(Exception):
    def __init__(self, message):
        self.message = message
        try:
            raise (Instance_Not_Available("Instance not available to create"))
            # Value of Exception is stored in error
        except Instance_Not_Available as error:
            print('Instance is not available :', error)



